"""Routes for results pages.

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

from flask import render_template, current_app, request

from fermo_gui.analysis.general_manager import GeneralManager
from fermo_gui.routes import bp


@bp.route("/results/<job_id>/", methods=["GET", "POST"])
def task_result(job_id: str):
    """Render the result dashboard page for the given job id.

    Returns:
        The result page or job_not_found

    Notes: All dashboard functionality should be called from
    fermo_gui.analysis.dashboard_manager
    """
    try:
        data = GeneralManager().read_data_from_json(
            str(Path(current_app.config.get("UPLOAD_FOLDER")).joinpath(job_id)), job_id
        )
    except FileNotFoundError:
        return render_template("job_not_found.html", data={"task_id": job_id})

    if request.method == "GET":
        # TODO(HEA, MMZ, 11.2.24): here comes the GET functionality (dashboard buildup)
        return render_template("dashboard.html", data=data)

    elif request.method == "POST":
        # TODO(HEA, MMZ, 11.2.24): here comes the POST functionality (triggers)
        return render_template("dashboard.html", data=data)
