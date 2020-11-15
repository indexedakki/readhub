from flask import Flask

from app import flask_app

# flask_app = Flask(__name__, template_folder='html')

if __name__ == '__main__':
    flask_app.run(debug = True, port=8501)