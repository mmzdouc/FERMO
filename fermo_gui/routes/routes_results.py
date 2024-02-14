"""Routes and logic for results pages.

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
from pathlib import Path
from typing import Union

from flask import render_template, current_app, request, redirect, url_for, Response

from fermo_gui.analysis.dashboard_manager import DashboardManager
from fermo_gui.analysis.general_manager import GeneralManager
from fermo_gui.routes import bp


@bp.route("/results/job_failed/<job_id>/")
def job_failed(job_id: str) -> Union[str, Response]:
    """Render the job_failed html.

    Assumes that every failed job should have a logfile; if not found, redirect to
    'job_not_found' page.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The job_failed page for the job ID or a redirect to 'job_not_found' page.
    """
    # TODO(MMZ 14.2.24): Cover with tests
    try:
        with open(
            Path(current_app.config.get("UPLOAD_FOLDER"))
            .joinpath(job_id)
            .joinpath(f"{job_id}.log"),
            "r",
        ) as logfile:
            log = logfile.read().split("\n")

        return render_template("job_failed.html", data={"task_id": job_id, "log": log})
    except FileNotFoundError:
        return redirect(url_for("routes.job_not_found", job_id=job_id))


@bp.route("/results/job_not_found/<job_id>/")
def job_not_found(job_id: str) -> str:
    """Render the job_not_found page.

    Logical end-point of job routes.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The job_not_found page for the job ID
    """
    # TODO(MMZ 14.2.24): Cover with tests
    return render_template("job_not_found.html", data={"task_id": job_id})


@bp.route("/results/<job_id>/", methods=["GET", "POST"])
def task_result(job_id: str) -> Union[str, Response]:
    """Render the result dashboard page for the given job id if found.

    Arguments:
        job_id: the job identifier, provided by the URL variable

    Returns:
        The dashboard page or the job_not_found page
    """
    # TODO(MMZ 14.2.24): Cover with tests
    try:
        f_sess = GeneralManager().read_data_from_json(
            str(Path(current_app.config.get("UPLOAD_FOLDER")).joinpath(job_id)),
            f"{job_id}.session.json",
        )
    except FileNotFoundError:
        return redirect(url_for("routes.job_not_found", job_id=job_id))

    if request.method == "GET":
        manager = DashboardManager()
        manager.get_dashboard_data(f_sess)
        return render_template("dashboard.html", data=manager.to_json_dict())
    #
    # elif request.method == "POST":
    #     # TODO(HEA, MMZ, 11.2.24): here comes the POST functionality (triggers)
    #     return render_template("dashboard.html", data=data)
