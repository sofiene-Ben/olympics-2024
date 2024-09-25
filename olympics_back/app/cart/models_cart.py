# from datetime import datetime
# from sqlalchemy import Enum, DECIMAL
# from config.db import db

# class Cart(db.Model):
#     __tablename__ = 'cart'
#     # __table_args__ = {'schema': 'cart_service'}

#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer, nullable=False)
#     # user_id = db.Column(db.String(255), nullable=False, index=True)  # Ajout de l'index pour les performances
#     # total_price = db.Column(DECIMAL(precision=10, scale=2), nullable=False)
#     # status = db.Column(Enum('Pending', 'Completed', 'Canceled', name='status_enum'), nullable=False, index=True)  # Ajout de l'index pour les performances
#     # created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     # updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

#     user_link = db.Column(db.String, db.ForeignKey('user.auth0_user_id'), nullable=False)
#     offer_link = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)

#     def __str__(self):
#         return '<Cart %r>' % self.id
    
# class Order(db.Model):
#     __tablename__ = 'order'
#     id = db.Column(db.Integer, primary_key=True)
#     quantity = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String, nullable=False)
#     payement_id = db.Column(db.String(1000), nullable=False)

#     user_link = db.Column(db.String, db.ForeignKey('user.auth0_user_id'), nullable=False)
#     offer_link = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
 
#     def __str__(self):
#         return '<Order %r>' % self.id

