from datetime import datetime
from sqlalchemy import Enum, DECIMAL
from config.db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    auth0_user_id = db.Column(db.String(255), unique=True, nullable=False)

    cart_items = db.relationship('Cart', backref=db.backref('user', lazy=True))
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))

    # def __init__(self, auth0_user_id):
    #     self.auth0_user_id = auth0_user_id


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    user_link = db.Column(db.String, db.ForeignKey('user.auth0_user_id'), nullable=False)
    offer_link = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)

    # def __str__(self):
    #     return '<Cart %r>' % self.id
    
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    payement_id = db.Column(db.String(1000), nullable=False)

    user_link = db.Column(db.String, db.ForeignKey('user.auth0_user_id'), nullable=False)
    offer_link = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
 
    # def __str__(self):
    #     return '<Order %r>' % self.id
    
class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    max_tickets = db.Column(db.Integer)
    price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)

    carts = db.relationship('Cart', backref=db.backref('offer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('offer', lazy=True))


    # def __str__(self):
    #     return '<Offer %r>' % self.name
    
