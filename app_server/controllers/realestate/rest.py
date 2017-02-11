from flask import Blueprint
from app_server.controllers.realestate.api_realestate import HomeItemList, StoreItemList, GroundItemList
from flask_restful import Api

bp_realestate = Blueprint('realestate', __name__, url_prefix='/api/realestate')
realestate_rest = Api(bp_realestate)

realestate_rest.add_resource(HomeItemList, '/home')
realestate_rest.add_resource(StoreItemList, '/store')
realestate_rest.add_resource(GroundItemList, '/ground')
