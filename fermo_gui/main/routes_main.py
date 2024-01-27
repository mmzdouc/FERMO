from flask import render_template

from fermo_gui.main import bp


@bp.route("/")
def index():
    """Render the index (landing) page of fermo_gui

    Returns:
        The index.html page as string.
    """
    return render_template("main/index.html")


@bp.route("/about/")
def about():
    """Render the about page of fermo_gui

    Returns:
        The about.html page as string.
    """
    return render_template("main/about.html")


@bp.route("/contact/")
def contact():
    """Render the contact page of fermo_gui

    Returns:
        The contact.html page as string.
    """
    return render_template("main/contact.html")


@bp.route("/help/")
def help():
    """Render the help page of fermo_gui

    Returns:
        The help.html page as string.
    """
    return render_template("main/help.html")
