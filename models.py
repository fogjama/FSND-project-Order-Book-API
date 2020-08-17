import os
from sqlalchemy import Column, DateTime, Float, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import datetime

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer = Column(Integer)
    value = Column(Float)
    date = Column(DateTime)

    def __init__(self, customer, value, date=datetime.datetime.now()):
        self.customer = customer
        self.value = value
        self.date = date
    
    def format(self):
        return {
            'id': self.id,
            'customer': self.customer,
            'value': self.value,
            'date': self.date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    delivery_date = Column(DateTime)

    def __init__(self, order, delivery_date):
        self.order = order,
        self.delivery_date = delivery_date
    
    def format(self):
        return {
            'id': self.id,
            'order': self.order,
            'delivery_date': self.delivery_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Customer(db.Model):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()