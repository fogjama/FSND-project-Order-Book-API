import os
import unittest
from flask_sqlalchemy import SQLAlchemy
import datetime

from app import create_app
from models import setup_db, Orders, Deliveries, Customers


class OrdersTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialise app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']

        # TODO: Define TEST_DATABASE_URL environment variable
        
        setup_db(self.app, self.database_path)

        # Bind the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            self.db.create_all()
        
        self.new_customer = {
            'name': 'John Smith'
        }

        self.new_order = {
            'customer': 1,
            'value': 22.50
        }

        self.new_delivery = {
            'order': 1,
            'delivery_date': datetime.datetime.now()
        }

    def tearDown(self):
        pass

    def test_create_customer(self):
        pass

    def test_create_order(self):
        pass

    def test_create_delivery(self):
        pass

    def test_get_paginated_orders(self):
        pass

    def test_get_order_by_id(self):
        pass

    def test_404_get_order_by_nonexistant_id(self):
        pass

    def test_get_customers(self):
        pass

    def test_get_customer_by_id(self):
        pass

    def test_404_get_customer_by_nonexistant_id(self):
        pass

    def test_get_paginated_deliveries(self):
        pass

    def test_get_delivery_by_id(self):
        pass

    def test_404_get_delivery_by_nonexistant_id(self):
        pass

    '''
    @TODO:
    add tests for 
    - post errors
    - patch success
    - patch errors
    - delete errors
    '''

    def test_delete_order(self):
        pass

    def test_delete_delivery(self):
        pass

    def test_delete_customer(self):
        pass

if __name__ == '__main__':
    unittest.main()