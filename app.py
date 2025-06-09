import os
from dotenv import load_dotenv
from flask import Flask, url_for, redirect
from markupsafe import escape
from flasgger import Swagger
from model import db, Post

load_dotenv()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
db.init_app(application)
Swagger(application)


@application.route("/")
def root():
    return redirect(url_for('flasgger.apidocs'))
