from flask import render_template

from fermo_gui.forms import bp


@bp.route("/")
def start_analysis():
    return render_template("forms/forms.html")
