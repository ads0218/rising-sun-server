from datetime import datetime
from app_server.common.instances.db import db


class Seller(db.Model):
    __tablename__ = 'seller'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    type = db.Column(db.String(64))
    name = db.Column(db.String(64))
    phone_number_1 = db.Column(db.String(32))
    phone_number_2 = db.Column(db.String(32))

    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'phone_number_1': self.phone_number_1,
            'phone_number_2': self.phone_number_2,
            'register_timestamp': self.register_timestamp
        }