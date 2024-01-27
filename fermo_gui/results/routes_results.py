from flask import render_template

from fermo_gui.results import bp


@bp.route("/example/")
def example():
    """Render the example result dashboard page of fermo_gui

    Returns:
        The results.html page as string.
    """
    return render_template("results/example.html")
