# -*- coding: utf-8 -*-

import os
import random
import sys
import time

import requests
from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app_server import create_app

app = create_app('config.default.Config')

from sqlalchemy.orm import sessionmaker
from app_server.common.instances.db import db
from app_server.models.home_model import Home

manager = Manager(app)
migrate = Migrate()
migrate.init_app(app, db, directory="./migrations")

server = Server(host="0.0.0.0", port=8082)
manager.add_command('db', MigrateCommand)


@manager.command
def initall():
    app.config['RUN'] = False
    createdb()

@manager.command
def createdb():
    db.init_app(app)
    db.create_all()


@manager.command
def dropdb():
    db.init_app(current_app)
    db.drop_all()

if __name__ == "__main__":
    manager.run()
