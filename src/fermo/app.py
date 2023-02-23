# external imports
from flask import Flask

# internal file imports
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True)
