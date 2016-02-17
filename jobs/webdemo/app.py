'''Search for job postings demonstration
Site main

@author Hideki Ikeda
@created Feb 16, 2016
'''

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('democonfig.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
