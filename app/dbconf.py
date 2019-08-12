from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
#from forms import CustomerForm

dbapp = Flask(__name__)
dbapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.sqlite3'
dbapp.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(dbapp)

if __name__ == '__main__':
    db.create_all()
