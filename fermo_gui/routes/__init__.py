from flask import Blueprint

bp = Blueprint("routes", __name__)

from fermo_gui.routes import routes_main
from fermo_gui.routes import routes_results
from fermo_gui.routes import routes_start_analysis
