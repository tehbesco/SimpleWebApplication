from __init__ import db

class Foods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    restaurant = db.Column(db.String(100), nullable=False)

class orderList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    name = db.Column(db.String(100))
    num = db.Column(db.String(100))
    area = db.Column(db.String(100))
    dri_name = db.Column(db.String(100))
    remarks = db.Column(db.String(100))
