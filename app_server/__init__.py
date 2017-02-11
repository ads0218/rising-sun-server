__version__ = '0.1dev'
"""
    rising-sun-room-server
    ~~~~

    서산시 부동산 통합 정보 사이트
    :writer: 2017 by daehyun Baek
"""

import hashlib
import eventlet

from datetime import timedelta
from flask import Flask
from flask_login import current_user
from flask_socketio import join_room
import cgitb
cgitb.enable(format='text')

eventlet.monkey_patch(socket=True, select=True)
hash_mod = hashlib.sha1()

def create_app(config_filepath='config.default.DevelopmentConfig'):
    """
    The main generator for the application.
    You need to create app with this method: ::

    >>> app = create_app()

    You can insert config path 'config_filepath'
    It create flask instance and set config, initialize external module with app
    and register flask blueprint on the current_app

    - bp_realestate : real estate blueprint

    :param config_filepath: the application config file path
    :type config_filepath: str

    :returns: application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_filepath)

    app.secret_key = app.config['SECRET_KEY']
    app.permanent_session_lifetime = timedelta(minutes=app.config['SESSION_ALIVE_MINUTES'])

    from redis import Redis
    rising_redis = Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])

    # logging module
    from app_server.common.instances.db import db
    db.init_app(app)

    from app_server.common.instances.login_manager import login_manager
    login_manager.init_app(app)

    from app_server.common.instances.celery import celery
    celery.init_app(app, 'config.celeryconfig.CeleryConfig')

    from app_server.models.home_model import Home
    from app_server.models.store_model import Store
    from app_server.models.ground_model import Ground
    from app_server.models.seller_model import Seller
    from app_server.models.realestate_model import Realestate
    from app_server.models.realestate_picture_model import RealestatePicture

    from app_server.controllers.realestate.rest import bp_realestate

    app.register_blueprint(bp_realestate)
    return app
