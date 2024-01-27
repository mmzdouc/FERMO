from flask import Blueprint

bp = Blueprint("main", __name__)

from fermo_gui.main import routes
