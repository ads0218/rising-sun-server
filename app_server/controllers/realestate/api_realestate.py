# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
import json
from flask import request, jsonify, current_app, session, abort
from flask_login import current_user, login_required
from sqlalchemy import asc, desc
from app_server.common.instances.db import db
from app_server.models.home_model import Home
from app_server.models.store_model import Store
from app_server.models.ground_model import Ground
from flask_restful import Resource, reqparse, marshal
from lxml import html
import codecs
from sqlalchemy import or_
from app_server.models.realestate_model import Realestate
from app_server.common.instances.db import db

class HomeItemList(Resource):

    def get(self):
        """
        주거 부동산 정보 요청
        """
        home_cate_list = ['일반원룸', '연립빌라', '단독', '다가구', '전원주택', '주거용 오피스텔', '단독/다가구', '아파트', '전원주택',
                          '빌라/연립', '아파트 분양권']
        home_list = db.session.query(Realestate).filter(Realestate.item_type.in_(home_cate_list)).all()
        home_list_json = [home.serialize for home in home_list]
        return jsonify({'results': home_list_json})


class StoreItemList(Resource):

    def get(self):
        """
        상가 부동산 정보 요청
        """

        store_list = db.session.query(Store).all()
        store_list_json = [store.serialize for store in store_list]
        return jsonify({'results': store_list_json})


class GroundItemList(Resource):

    def get(self):
        """
        토지 부동산 정보 요청
        """

        ground_list = db.session.query(Ground).all()
        ground_list_json = [ground.serialize for ground in ground_list]
        return jsonify({'results': ground_list_json})

