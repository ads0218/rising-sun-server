from app_server.common.instances.db import db
from datetime import datetime

class RealestatePicture(db.Model):
    __tablename__ = 'realestate_picture'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    picture_file_name = db.Column(db.String(64))
    picture_url = db.Column(db.String(64))
    realestate_id = db.Column(db.Integer, db.ForeignKey('realestate.id'))

    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    realestate = db.relationship('Realestate')

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