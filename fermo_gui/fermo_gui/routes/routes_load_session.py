"""Routes for session file loading

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

import shutil
from pathlib import Path
from typing import Union

from flask import Response, current_app, flash, redirect, render_template, url_for
from werkzeug.utils import secure_filename

from fermo_gui.analysis.general_manager import GeneralManager as GenManager
from fermo_gui.analysis.session_processor import SessionProcessor
from fermo_gui.forms.session_load_forms import SessionLoadForm
from fermo_gui.routes import bp


def setup_session_load(form: SessionLoadForm) -> Union[str, Response]:
    """Set up conditions for loading a fermo session file

    Arguments:
        form: the filled SessionLoadForm instance

    Returns:
        Either a Response or a rendered html as str
    """
    location = current_app.config.get("UPLOAD_FOLDER")
    task_id = GenManager().create_uuid(location)
    task_path = Path(location).joinpath(task_id)
    task_path_results = task_path.joinpath("results")
    task_path_results.mkdir(parents=True)

    try:
        processor = SessionProcessor(
            form=form,
            task_dir=task_path_results,
            online=current_app.config.get("ONLINE"),
        )
        processor.run_processor()
    except Exception as e:
        flash(str(e))
        if task_path.exists():
            shutil.rmtree(task_path, ignore_errors=True)
        return render_template("load_session.html", form=form)

    return redirect(url_for("routes.task_result", job_id=task_id))


def redirect_existing_job(form: SessionLoadForm) -> Union[str, Response]:
    """Perform checks and redirect to results

    Arguments:
        form: the filled SessionLoadForm instance

    Returns:
        Either a Response or a rendered html as str
    """
    job_id = secure_filename(form.reload_existing_jobid.data)
    if Path(current_app.config.get("UPLOAD_FOLDER")).joinpath(job_id).exists():
        return redirect(url_for("routes.task_result", job_id=job_id))
    else:
        flash(
            f"Could not find FERMO job ID '{job_id}' in the "
            f"results files. This could be due to a typo (e.g. a trailing space) or "
            f"because the job was removed (jobs are only retained for 30 days)."
        )
        return render_template("load_session.html", form=form)


@bp.route("/analysis/load_session/", methods=["GET", "POST"])
def load_session() -> Union[str, Response]:
    """Render load session page, get and store data, load.

    Returns:
        Either a Response or a rendered html string
    """
    form = SessionLoadForm()

    if form.validate_on_submit():
        if (
            form.reload_existing_jobid.data is not None
            and form.reload_existing_jobid.data != ""
        ):
            return redirect_existing_job(form=form)
        elif form.session_file.data is not None:
            return setup_session_load(form=form)
        else:
            flash("No valid job ID nor a FERMO Session file were provided.")
            return render_template("load_session.html", form=form)

    return render_template("load_session.html", form=form)
