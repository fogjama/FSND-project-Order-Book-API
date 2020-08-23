import os
import unittest
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
import os

from app import create_app
from models import setup_db, Order, Delivery, Customer

admin_token = os.environ['ADMIN_TOKEN']
user_token = os.environ['USER_TOKEN']
auth_admin = {'Authorization': f'Bearer {admin_token}'}
auth_user = {'Authorization': f'Bearer {user_token}'}
auth_malformed = {'Authorization': 'Basic'}

class OrdersTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialise app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

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
        res = self.client().post('/customers', headers=auth_admin, json=self.new_customer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_order(self):
        res = self.client().post('/orders', headers=auth_admin, json=self.new_order)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_delivery(self):
        res = self.client().post('/deliveries', headers=auth_admin, json=self.new_delivery)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_order_bad_request(self):
        res = self.client().post('/orders', headers=auth_admin, json={'name': False})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_customer_bad_request(self):
        res = self.client().post('/customers', headers=auth_admin, json={'active': False})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_create_delivery_bad_request(self):
        res = self.client().post('/deliveries', headers=auth_admin, json={'name': 'wombat'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
    
    # RBAC tests on Create

    def test_create_order_missing_auth(self):
        res = self.client().post('/orders', headers=auth_user, json={'name': False})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_create_order_malformed_auth(self):
        res = self.client().post('/orders', headers=auth_malformed, json=self.new_order)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Test Get

    def test_get_paginated_orders(self):
        res = self.client().get('/orders', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['orders'])
        self.assertTrue(data['total_orders'])

    def test_get_order_by_id(self):
        res = self.client().get('/orders/1', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['order']['id'])
        self.assertTrue(data['order']['value'])
        self.assertTrue(data['order']['date'])
        self.assertTrue(data['order']['customer'])

    def test_404_get_order_by_nonexistant_id(self):
        res = self.client().get('orders/100000', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_paginated_customers(self):
        res = self.client().get('/customers', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customers'])
        self.assertTrue(data['total_customers'])

    def test_get_customer_by_id(self):
        res = self.client().get('/customers/1', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customer']['id'])
        self.assertTrue(data['customer']['name'])

    def test_404_get_customer_by_nonexistant_id(self):
        res = self.client().get('/customers/1000000', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_paginated_deliveries(self):
        res = self.client().get('/deliveries', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deliveries'])
        self.assertTrue(data['total_deliveries'])

    def test_get_delivery_by_id(self):
        res = self.client().get('/deliveries/1', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delivery']['id'])
        self.assertTrue(data['delivery']['order'])
        self.assertTrue(data['delivery']['delivery_date'])

    def test_404_get_delivery_by_nonexistant_id(self):
        res = self.client().get('/deliveries/1000000', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_orders_by_customer(self):
        res = self.client().get('/customers/1/orders', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['orders'])
        self.assertTrue(data['total_orders'])

    def test_404_get_orders_by_nonexistant_customer(self):
        res = self.client().get('/customers/1000000/orders', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_deliveries_by_order(self):
        res = self.client().get('/orders/1/deliveries', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deliveries'])
        self.assertTrue(data['total_deliveries'])

    def test_404_get_deliveries_by_nonexistant_order(self):
        res = self.client().get('/orders/1000000/deliveries', headers=auth_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test Patch

    def test_update_customer(self):
        res = self.client().patch('/customers/1', headers=auth_admin, json={'name': 'Walla Wanga'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['customer'])

    def test_update_order(self):
        res = self.client().patch('/orders/1', headers=auth_admin, json={'value': 99.99})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['order'])

    def test_404_update_customer(self):
        res = self.client().patch('/customers/10000000', headers=auth_admin, json={'name': 'Jodie Foster'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_update_order(self):
        res = self.client().patch('/orders/10000000', headers=auth_admin, json={'value': 99.99})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_405_update_delivery(self):
        res = self.client().patch('/deliveries/1', headers=auth_admin, json={'order': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Test Delete

    def test_delete_order(self):
        res = self.client().delete('/orders/3', headers=auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_delete_delivery(self):
        res = self.client().delete('/deliveries/3', headers=auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_404_delete_order(self):
        res = self.client().delete('/orders/100000000', headers=auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_delete_delivery(self):
        res = self.client().delete('/deliveries/100000000', headers=auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_405_delete_customer(self):
        res = self.client().delete('/customers/1000000000', headers=auth_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)


if __name__ == '__main__':

    unittest.main()