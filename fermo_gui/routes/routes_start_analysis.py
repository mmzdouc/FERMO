"""Routes for pages related to data input and processing.

Copyright (c) 2022-present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import shutil
from pathlib import Path
from typing import Union

from celery.result import AsyncResult
from flask import (
    Response,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from fermo_gui.analysis.fermo_core_manager import start_fermo_core_manager
from fermo_gui.analysis.general_manager import GeneralManager as GenManager
from fermo_gui.analysis.input_processor import InputProcessor
from fermo_gui.config.extensions import socketio
from fermo_gui.forms.analysis_input_forms import AnalysisForm
from fermo_gui.routes import bp


@bp.route("/analysis/start_analysis/", methods=["GET", "POST"])
def start_analysis() -> Union[str, Response]:
    """Render start analysis page, get and store data, init analysis.

    Notes: On every GET, the page prepares a new job (job ID + upload directory)
    On POST (form.validate_on_submit()), the asynchronous job is started

    Returns:
        On GET, the "start_analysis" page, on POST a redirect to the "job_submitted" p.
    """
    form = AnalysisForm()

    if form.validate_on_submit():
        task_id = GenManager().create_uuid(current_app.config.get("UPLOAD_FOLDER"))
        task_path = Path(current_app.config.get("UPLOAD_FOLDER")).joinpath(task_id)
        task_path.mkdir()

        try:
            processor = InputProcessor(
                form=form,
                task_dir=Path(task_path),
                root_url=request.base_url.partition("/analysis/start_analysis/")[0],
            )
            processor.run_processor()
            parameters_dict = processor.return_params()
            with open(f"{task_path}/{task_id}.parameters.json", "w") as outfile:
                outfile.write(json.dumps(parameters_dict, indent=2, ensure_ascii=False))
        except Exception as e:
            flash(str(e))
            if task_path.exists():
                shutil.rmtree(task_path, ignore_errors=True)
            return render_template("start_analysis.html", form=form)

        metadata = {
            "job_id": task_id,
            "task_path": str(task_path.resolve()),
            "email": form.email.data if len(form.email.data) != 0 else None,
            "email_notify": (
                True if (len(form.email.data) != 0 and processor.online) else False
            ),
            "root_url": request.base_url.partition("/analysis/start_analysis/")[0],
        }

        start_fermo_core_manager.apply_async(
            kwargs={"metadata": metadata},
            task_id=metadata["job_id"],
        )
        return redirect(url_for("routes.job_submitted", job_id=metadata["job_id"]))

    return render_template("start_analysis.html", form=form)


@bp.route("/analysis/job_submitted/<job_id>/", methods=["GET"])
def job_submitted(job_id: str) -> str:
    """Serves as placeholder during calculation.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The rendered "job_submitted.html" page
    """
    job_data = {
        "task_id": job_id,
        "root_url": request.base_url.partition("/analysis/job_submitted/")[0],
    }
    return render_template("job_submitted.html", job_data=job_data)


@socketio.on("startup_event")
def handle_startup_message(data: dict):
    """Debug function to check responsiveness of socket.io

    Arguments:
        data: a JSON-derived dictionary
    """
    print("received json: " + str(data))


@socketio.on("get_status")
def check_job_status(data: dict):
    """Serve job status upon request.

    Note: Celery does not differentiate between non-existing and non-running jobs.
    To prevent endless loops on non-existing jobs, existence of upload folder is
    verified: no folder, no job run

    Arguments:
        data: JSON-derived dict with job ID to check status of
    """
    if (
        not Path(current_app.config.get("UPLOAD_FOLDER"))
        .joinpath(data.get("task_id"))
        .exists()
    ):
        socketio.emit("job_status", {"status": "job_not_found"})
    else:
        try:
            result = AsyncResult(data.get("task_id"))
            outcome = result.result if result.ready() else None
            match outcome:
                case True:
                    socketio.emit("job_status", {"status": "job_successful"})
                case False:
                    socketio.emit("job_status", {"status": "job_failed"})
                case None:
                    socketio.emit("job_status", {"status": "job_running"})
        except ValueError:
            socketio.emit("job_status", {"status": "job_not_found"})
