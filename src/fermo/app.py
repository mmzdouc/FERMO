# external imports
from flask import Flask
import toml

# internal file imports
from views import views


# initialize the app
app = Flask(__name__)
app.config.from_file('config.toml', load=toml.load)
app.register_blueprint(views, url_prefix="/")
app.testing = False

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=False)
