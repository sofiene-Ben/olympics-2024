# from config.db import db

# class User(db.Model):
#     __tablename__ = 'user'

#     id = db.Columnn(db.Integer, Primary_key=True)
#     auth0_user_id = db.Column(db.String(255), unique=True, nullable=False)

#     cart_items = db.relationship('Cart', backref=db.backref('user', lazy=True))
#     orders = db.relationship('Order', backref=db.backref('user', lazy=True))

# def __str__(self):
#     return '<User %r>' % User.auth0_user_id