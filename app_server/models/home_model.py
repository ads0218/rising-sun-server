from datetime import datetime
from app_server.common.instances.db import db
from .realestate_model import Realestate

class Home(Realestate):
    __tablename__ = 'home'

    id = db.Column(db.Integer, db.ForeignKey('realestate.id'), primary_key=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'price': self.price,
            'size': self.size,
            'description': self.description,
            'register_timestamp': self.register_timestamp
        }
