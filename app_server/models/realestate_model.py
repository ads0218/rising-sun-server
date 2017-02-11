from datetime import datetime
from app_server.common.instances.db import db

class Realestate(db.Model):
    __tablename__ = 'realestate'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    item_type = db.Column(db.String(64))
    sale_type = db.Column(db.String(64))

    source = db.Column(db.String(32))
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    address = db.Column(db.String(128))

    price = db.Column(db.String(64), index=True)
    size = db.Column(db.String(64), index=True)

    contact = db.Column(db.String(128))
    floor = db.Column(db.String(64))

    link = db.Column(db.String(128))
    description = db.Column(db.Text)
    title = db.Column(db.String(128))
    register_date = db.Column(db.String(64))
    # seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    register_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # seller = db.relationship('Seller', lazy="joined")
    # realestate_picture_list = db.relationship('RealestatePicture', lazy='joined')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'item_type': self.item_type,
            'sale_type': self.sale_type,

            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,

            'price': self.price,
            'size': self.size,

            'contact': self.contact,
            'floor': self.floor,
            # 'seller': self.seller.serialize if self.seller is not None else None,
            # 'realestate_picture_list': [ realestate_picture.serialize
            #                              for realestate_picture in self.realestate_picture_list ],

            'description': self.description,
            'register_date': self.register_date,
            'register_timestamp': self.register_timestamp
        }
