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
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from fermo_gui.analysis.fermo_core_manager import start_fermo_core_manager
from fermo_gui.analysis.general_manager import GeneralManager as GenManager
from fermo_gui.config.extensions import socketio
from fermo_gui.forms.analysis_input_forms import AnalysisInput
from fermo_gui.routes import bp


def prepare_dummy_run(job_id: str):
    """Write dummy data to see if logic works"""
    shutil.copy(
        src=Path("fermo_gui/upload/example/data/quant_all.csv"),
        dst=Path(f"fermo_gui/upload/{job_id}/quant_all.csv"),
    )

    shutil.copy(
        src=Path("fermo_gui/upload/example/data/msms.mgf"),
        dst=Path(f"fermo_gui/upload/{job_id}/msms.mgf"),
    )

    data = {
        "files": {
            "peaktable": {
                "filepath": f"fermo_gui/upload/{job_id}/quant_all.csv",
                "format": "mzmine3",
                "polarity": "positive",
            },
            "msms": {
                "filepath": f"fermo_gui/upload/{job_id}/msms.mgf",
                "format": "mgf",
                "rel_int_from": 0.01,
            },
        },
        "core_modules": {
            "adduct_annotation": {"activate_module": False},
            "neutral_loss_annotation": {"activate_module": False},
            "fragment_annotation": {"activate_module": False},
            "spec_sim_networking": {
                "modified_cosine": {
                    "activate_module": True,
                    "msms_min_frag_nr": 5,
                    "fragment_tol": 0.1,
                    "score_cutoff": 0.7,
                    "max_nr_links": 10,
                    "maximum_runtime": 200,
                }
            },
        },
        "additional_modules": {
            "feature_filtering": {
                "activate_module": True,
                "filter_rel_area_range": [0.9, 1.0],
            },
            "ms2query_annotation": {
                "activate_module": True,
                "score_cutoff": 0.7,
                "maximum_runtime": 1200,
            },
        },
    }
    with open(Path(f"fermo_gui/upload/{job_id}/parameters.json"), "w") as outfile:
        outfile.write(json.dumps(data, indent=4, ensure_ascii=False))


@bp.route("/analysis/start_analysis/", methods=["GET", "POST"])
def start_analysis() -> Union[str, Response]:
    """Render start analysis page, get and store data, init analysis.

    Notes: On every GET, the page prepares a new job (job ID + upload directory)
    On POST (form.validate_on_submit()), the asynchronous job is started

    Returns:
        On GET, the "start_analysis" page, on POST a redirect to the "job_submitted" p.
    """
    form = AnalysisInput()

    if request.method == "GET":
        task_id = GenManager().create_uuid(current_app.config.get("UPLOAD_FOLDER"))
        task_upload_path = GenManager().create_upload_dir(
            current_app.config.get("UPLOAD_FOLDER"), task_id
        )
        session["task_id"] = task_id
        session["task_upload_path"] = task_upload_path
        return render_template("start_analysis.html", form=form)

    if form.validate_on_submit():
        metadata = {
            "job_id": session["task_id"],
            "email": "mmzdouc@gmail.com",
            "email_notify": False,
        }

        prepare_dummy_run(session["task_id"])

        # TODO(MMZ 26.05.): turn on email notification
        # root_url = request.base_url.partition("/analysis/start_analysis/")[0]
        # if "localhost" in root_url or "127.0.0.1" in root_url:
        #     metadata["email_notify"] = False
        # elif metadata.get("email") is None:
        #     metadata["email_notify"] = False
        # elif current_app.config.get("MAIL_USERNAME") is None:
        #     metadata["email_notify"] = False

        start_fermo_core_manager.apply_async(
            kwargs={"metadata": metadata},
            task_id=metadata["job_id"],
        )
        return redirect(url_for("routes.job_submitted", job_id=metadata["job_id"]))


@bp.route("/analysis/job_submitted/<job_id>/", methods=["GET"])
def job_submitted(job_id: str) -> str:
    """Serves as placeholder during calculation.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The rendered "job_submitted.html" page
    """
    # TODO(MMZ 14.2.24): Cover with tests
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
    # TODO(MMZ 14.2.24): Cover with tests
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
