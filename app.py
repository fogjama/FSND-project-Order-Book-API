import os
from flask import Flask, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import sys

from models import Order, Customer, Delivery, setup_db
from auth.auth import AuthError, requires_auth


ITEMS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    items = [item.format() for item in selection]
    paginated_items = items[start:end]

    return paginated_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # POST endpoints
    @app.route('/customers', methods=['POST'])
    @requires_auth('post:customers')
    def create_customer(jwt):
        customer = request.get_json()

        if 'name' not in customer:
            abort(400)

        try:
            if 'active' in customer:
                new_customer = Customer(
                    name=customer['name'],
                    active=customer['active']
                )
            else:
                new_customer = Customer(
                    name=customer['name']
                )

            new_customer.insert()

            return jsonify({
                'success': True,
                'customer': new_customer.format()
            })

        except BaseException:
            abort(422)

    @app.route('/orders', methods=['POST'])
    @requires_auth('post:orders')
    def create_order(jwt):
        order = request.get_json()

        for key in ['customer', 'value']:
            if key not in order:
                abort(400)
                break

        if 'date' in order:
            new_order = Order(
                customer=order['customer'],
                value=order['value'],
                date=order['date']
            )
        else:
            new_order = Order(
                customer=order['customer'],
                value=order['value']
            )

        new_order.insert()

        return jsonify({
            'success': True,
            'order': new_order.format()
        })


    @app.route('/deliveries', methods=['POST'])
    @requires_auth('post:deliveries')
    def create_delivery(jwt):
        delivery = request.get_json()

        for key in ['order', 'delivery_date']:
            if key not in delivery:
                abort(400)
                break

        new_delivery = Delivery(
            order=delivery['order'],
            delivery_date=delivery['delivery_date']
        )
        new_delivery.insert()

        return jsonify({
            'success': True,
            'delivery': new_delivery.format()
        })


    # PATCH endpoints
    @app.route('/customers/<customer_id>', methods=['PATCH'])
    @requires_auth('update:customers')
    def update_customer(jwt, customer_id):
        customer = request.get_json()

        customer_db = Customer.query.filter(
            Customer.id == int(customer_id)).one_or_none()

        if customer_db is None:
            abort(404)

        if 'name' in customer:
            customer_db.name = customer['name']
            customer_db.update()

        if 'active' in customer:
            customer_db.active = customer['active']
            customer_db.update()

        return jsonify({
            'success': True,
            'customer': customer_db.format()
        })


    @app.route('/orders/<order_id>', methods=['PATCH'])
    @requires_auth('update:orders')
    def update_order(jwt, order_id):
        order = request.get_json()

        order_db = Order.query.filter(
            Order.id == int(order_id)).one_or_none()

        if order_db is None:
            abort(404)

        if 'customer' in order:
            order_db.customer = order['customer']
            order_db.update()

        if 'value' in order:
            order_db.value = order['value']
            order_db.update()

        return jsonify({
            'success': True,
            'order': order_db.format()
        })


    # Delivery cannot be PATCHed

    # DELETE endpoints
    @app.route('/orders/<order_id>', methods=['DELETE'])
    @requires_auth('delete:orders')
    def delete_order(jwt, order_id):

        try:
            order = Order.query.filter(Order.id == int(order_id)).one_or_none()

            if order is None:
                abort(404)

            order.delete()

            return jsonify({
                'success': True,
                'deleted': order_id
            })

        except BaseException:
            abort(404)

    @app.route('/deliveries/<delivery_id>', methods=['DELETE'])
    @requires_auth('delete:deliveries')
    def delete_delivery(jwt, delivery_id):

        try:
            delivery = Delivery.query.filter_by(
                id=delivery_id).one_or_none()

            if delivery is None:
                abort(404)

            delivery.delete()

            return jsonify({
                'success': True,
                'deleted': delivery_id
            })
        
        except BaseException as e:
            abort(404)

    # Customer cannot be DELETEd; PATCH 'active' to False

    @app.route('/orders', methods=['GET'])
    @requires_auth('read:orders')
    def get_order_list(jwt):
        selection = Order.query.order_by(Order.id).all()
        orders = paginate_results(request, selection)

        total_orders = len(selection)

        return jsonify({
            'success': True,
            'orders': orders,
            'total_orders': total_orders
        })

    @app.route('/orders/<order_id>', methods=['GET'])
    @requires_auth('read:orders')
    def get_order(jwt, order_id):
        order = Order.query.filter_by(id=order_id).one_or_none()

        if order is None:
            abort(404)

        return jsonify({
            'success': True,
            'order': order.format()
        })

    @app.route('/customers', methods=['GET'])
    @requires_auth('read:customers')
    def get_customer_list(jwt):
        selection = Customer.query.order_by(Customer.name).all()
        customers = paginate_results(request, selection)

        total_customers = len(selection)

        return jsonify({
            'success': True,
            'customers': customers,
            'total_customers': total_customers
        })

    @app.route('/customers/<customer_id>', methods=['GET'])
    @requires_auth('read:customers')
    def get_customer(jwt, customer_id):
        customer = Customer.query.filter_by(id=customer_id).one_or_none()

        if customer is None:
            abort(404)

        return jsonify({
            'success': True,
            'customer': customer.format()
        })

    @app.route('/deliveries', methods=['GET'])
    @requires_auth('read:deliveries')
    def get_delivery_list(jwt):
        selection = Delivery.query.order_by(Delivery.id).all()
        deliveries = paginate_results(request, selection)

        total_deliveries = len(selection)

        return jsonify({
            'success': True,
            'deliveries': deliveries,
            'total_deliveries': total_deliveries
        })

    @app.route('/deliveries/<delivery_id>', methods=['GET'])
    @requires_auth('read:deliveries')
    def get_delivery(jwt, delivery_id):
        delivery = Delivery.query.filter_by(id=delivery_id).one_or_none()

        if delivery is None:
            abort(404)

        return jsonify({
            'success': True,
            'delivery': delivery.format()
        })

    @app.route('/customers/<customer_id>/orders', methods=['GET'])
    @requires_auth('read:orders')
    def get_orders_by_customer(jwt, customer_id):
        customer = Customer.query.filter_by(id=customer_id).one_or_none()

        if customer is None:
            abort(404)

        selection = Order.query.filter_by(customer=customer_id).all()
        orders = paginate_results(request, selection)

        total_orders = len(selection)

        return jsonify({
            'success': True,
            'orders': orders,
            'total_orders': total_orders
        })

    @app.route('/orders/<order_id>/deliveries', methods=['GET'])
    @requires_auth('read:deliveries')
    def get_deliveries_by_order(jwt, order_id):
        order = Order.query.filter_by(id=order_id).one_or_none()

        if order is None:
            abort(404)
        
        selection = Delivery.query.filter_by(order=order_id).all()
        deliveries = paginate_results(request, selection)

        total_deliveries = len(selection)

        return jsonify({
            'success': True,
            'deliveries': deliveries,
            'total_deliveries': total_deliveries
        })

    # Error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = error.get_response()
        response.data = json.dumps({
            'success': False,
            'error': error.code,
            'message': error.name
        })
        response.content_type = 'application/json'
        return response
    
    @app.errorhandler(AuthError)
    def auth_error(error):
        if error.status_code == 401:
            return jsonify({
                'success': False,
                'error': 401,
                'message': error.error['description']
            }), 401
        
        elif error.status_code == 403:
            return jsonify({
                'success': False,
                'error': 403,
                'message': 'Forbidden: Missing authorization'
            }), 403
        
        else:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Bad request'
            }), 400

    return app


app = create_app()

# Run sequence for testing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# Run sequence for productive use
# if __name__ == '__main__':
#     app.run()
