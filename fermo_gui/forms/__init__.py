from flask import Blueprint

bp = Blueprint("forms", __name__)

from fermo_gui.forms import routes
