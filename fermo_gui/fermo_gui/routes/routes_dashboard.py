"""Provides Flask Blueprints instances.

Copyright (c) 2024-present Hannah Esther Augustijn, MSc

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

from flask import Response, current_app, jsonify, redirect, send_file, url_for

from fermo_gui.routes import bp


@bp.route("/download/<job_id>/<filename>")
def download_file(job_id: str, filename: str) -> Union[Response, tuple[Response, int]]:
    """Render download for given job id and download filename

    Returns:
        The download file.
    """
    download_f = (
        Path(current_app.config.get("UPLOAD_FOLDER"))
        .joinpath(job_id)
        .joinpath("results")
        .joinpath(filename)
    )
    download_f = download_f.resolve()
    if not download_f.exists():
        return jsonify({"error": "File not found"}), 404

    return send_file(download_f, as_attachment=True)


@bp.route("/check_file/<job_id>/<filename>")
def check_file(job_id: str, filename: str) -> Response:
    """Check if the given file exists for the given job id"""
    download_f = (
        Path(current_app.config.get("UPLOAD_FOLDER"))
        .joinpath(job_id)
        .joinpath("results")
        .joinpath(filename)
    )
    download_f = download_f.resolve()
    if download_f.exists():
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})
