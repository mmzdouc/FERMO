# external imports
from flask import Flask

# internal file imports
from views import views


# initialize the app 
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run()
