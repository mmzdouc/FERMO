"""Application factory of fermo_gui Flask app.

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

import contextlib
import os
from importlib import metadata
from typing import Optional

from flask import Flask

from fermo_gui.config.config_celery import configure_celery
from fermo_gui.config.config_mail import configure_mail
from fermo_gui.config.config_session import configure_session
from fermo_gui.config.extensions import mail, session, socketio
from fermo_gui.routes import bp


def create_app(test_config: Optional[dict] = None) -> Flask:
    """Factory function for Flask app, automatically detected by Flask.

    Arguments:
        test_config: mapping of app configuration for testing purposes

    Returns:
        An instance of the Flask object
    """
    app = Flask(__name__, instance_relative_config=True)
    app = configure_app(app, test_config)
    app = configure_session(app)
    app = configure_mail(app)
    app = configure_celery(app)

    session.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)

    create_instance_path(app)
    register_context_processors(app)
    app.register_blueprint(bp)
    return app


def configure_app(app: Flask, test_config: Optional[dict] = None) -> Flask:
    """Configure the Flask app.

    Arguments:
        app: The Flask app instance
        test_config: mapping of app configuration for testing purposes
    """
    app.config["SECRET_KEY"] = "dev"
    app.config["UPLOAD_FOLDER"] = "fermo_gui/upload/"
    app.config["ALLOWED_EXTENSIONS"] = {"json", "csv", "mgf", "session"}
    app.config["ONLINE"] = False
    app.config["MAX_RUN_TIME"] = None

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    return app


def create_instance_path(app: Flask):
    """Create the instance path for the Flask app if not available.

    Arguments:
        app: The Flask app instance
    """
    with contextlib.suppress(OSError):
        os.makedirs(app.instance_path)


def register_context_processors(app: Flask):
    """Register context processors to get access to variables across all pages.

    Arguments:
        app: The Flask app instance
    """

    @app.context_processor
    def set_version() -> dict:
        return {"version": metadata.version("fermo_gui")}
