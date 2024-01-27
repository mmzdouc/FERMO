from flask import Blueprint

bp = Blueprint("results", __name__)

from fermo_gui.results import routes_results
