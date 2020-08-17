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

    # Test Post

    def test_create_customer(self):
        pass

    def test_create_order(self):
        pass

    def test_create_delivery(self):
        pass

    def test_create_order_error(self):
        pass

    def test_create_customer_error(self):
        pass

    def test_create_delivery_error(self):
        pass

    # Test Get

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

    def test_get_orders_by_customer(self):
        pass

    def test_get_deliveries_by_order(self):
        pass

    # Test Patch

    def test_update_customer(self):
        pass

    def test_update_order(self):
        pass

    def test_update_delivery(self):
        pass

    def test_404_update_customer(self):
        pass

    def test_404_update_order(self):
        pass

    def test_404_update_delivery(self):
        pass

    # Test Delete

    def test_delete_order(self):
        pass

    def test_delete_delivery(self):
        pass

    def test_delete_customer(self):
        pass

    def test_404_delete_order(self):
        pass

    def test_404_delete_customer(self):
        pass

    def test_404_delete_delivery(self):
        pass


if __name__ == '__main__':
    unittest.main()