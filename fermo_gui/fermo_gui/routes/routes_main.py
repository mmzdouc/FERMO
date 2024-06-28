"""Routes for main and auxiliary pages.

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

from flask import current_app, render_template

from fermo_gui.routes import bp


@bp.route("/")
def index() -> str:
    """Render the index (landing) page of fermo_gui

    Returns:
        The index.html page as string.
    """
    online = current_app.config.get("ONLINE") or False
    return render_template("index.html", online=online)


@bp.route("/about/")
def about() -> str:
    """Render the about page of fermo_gui

    Returns:
        The about.html page as string.
    """
    return render_template("about.html")


@bp.route("/contact/")
def contact() -> str:
    """Render the contact page of fermo_gui

    Returns:
        The contact.html page as string.
    """
    return render_template("contact.html")


@bp.route("/help/")
def help() -> str:
    """Render the help page of fermo_gui

    Returns:
        The help.html page as string.
    """
    return render_template("help.html")
