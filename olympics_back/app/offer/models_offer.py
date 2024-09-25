# from config.db import db

# class Offer(db.Model):
#     __tablename__ = 'offer'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     max_tickets = db.Column(db.Integer)
#     price = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)

#     carts = db.relationship('Cart', backref=db.backref('offer', lazy=True))
#     orders = db.relationship('Order', backref=db.backref('offer', lazy=True))
    

#     def __str__(self):
#         return '<Offer %r>' % self.name