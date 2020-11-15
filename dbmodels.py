from flask_login import UserMixin
from wtforms.fields.core import SelectField
from database import db



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))
    Phone = db.Column(db.String(1000))
    # Gender = SelectField('Gender', choices=[('Male'),('Female'),('Others')])

class contact(UserMixin, db.Model):
    __tablename__ = 'contact'
    __bind_key__ = 'contact'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    #email = db.Column(db.String(100), unique=True)
    #password = db.Column(db.String(100))
    #message = db.Column(db.String(1000))
    Name = db.Column(db.String(1000))
    Email = db.Column(db.String(1000))
    Phone_Number = db.Column(db.String(1000))
    Message = db.Column(db.String(1000))

class issuebook(UserMixin, db.Model):
    __tablename__ = 'issuebook'
    __bind_key__ = 'issuebook'
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Name = db.Column(db.String(1000))
    ISBN = db.Column(db.String(1000))
    Title = db.Column(db.String(1000))
    Author = db.Column(db.String(1000))
    Edition = db.Column(db.String(1000))
    Email = db.Column(db.String(1000))