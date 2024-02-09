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

from celery import uuid
from flask import render_template, redirect, url_for, session, Response

from fermo_gui.analysis.analysis_manager import FermoAnalysisManager as Manager
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
        task_id = uuid()
        task = Manager().slow_add_dummy.apply_async(
            kwargs={
                "x": 2,
                "y": 2,
                "job_id": task_id,
            },
            task_id=task_id,
        )

        session["task_id"] = task.id
        session["start_time"] = datetime.now().replace(microsecond=0)

        return redirect(url_for("routes.job_submitted"))

    return render_template("start_analysis.html", form=form)


@bp.route("/analysis/job_submitted/")
def job_submitted():
    """Render the job_submitted page, serving as placeholder during calculation.

    Returns:
        The rendered job_submitted.html page as string
    """
    return render_template("job_submitted.html", session=session)
