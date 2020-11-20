from flask import Flask
from database import db
from app import app

# flask_app = Flask(__name__, template_folder='html')


app = Flask(__name__, template_folder='html')
#Bootstrap(flask_app)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
app.config['SQLALCHEMY_BINDS'] = {
    'contact': 'sqlite:///database/contact.db',
    'issuebook': 'sqlite:///database/issuebook.db'
                                       }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
