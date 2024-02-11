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
from datetime import datetime
from typing import Union

from flask import render_template, redirect, url_for, session, Response, current_app

from fermo_gui.analysis.analysis_manager import start_fermo_core
from fermo_gui.analysis.general_manager import GeneralManager as GenManager
from fermo_gui.forms.analysis_input_forms import AnalysisInput
from fermo_gui.routes import bp


@bp.route("/analysis/start_analysis", methods=["GET", "POST"])
def start_analysis() -> Union[str, Response]:
    """Render start analysis page, get and store data, init analysis.

    Returns:
        The rendered start_analysis.html page as string
    """
    form = AnalysisInput()

    if form.validate_on_submit():
        GenManager.store_data_as_json(
            session["task_upload_path"], session["task_id"], {"email": form.email.data}
        )

        start_fermo_core.apply_async(
            kwargs={
                "job_id": session["task_id"],
                "upload_path": session["task_upload_path"],
            },
            task_id=session["task_id"],
        )
        session["start_time"] = datetime.now().replace(microsecond=0)
        return redirect(url_for("routes.job_submitted"))

    task_id = GenManager().create_uuid(current_app.config.get("UPLOAD_FOLDER"))
    task_upload_path = GenManager().create_upload_dir(
        current_app.config.get("UPLOAD_FOLDER"), task_id
    )
    session["task_id"] = task_id
    session["task_upload_path"] = task_upload_path

    return render_template("start_analysis.html", form=form)


@bp.route("/analysis/job_submitted/")
def job_submitted():
    """Render the job_submitted page, serving as placeholder during calculation.

    Returns:
        The rendered job_submitted.html page as string
    """
    return render_template("job_submitted.html", session=session)
