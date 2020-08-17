import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route('/customers', methods=['POST'])
  def create_customer():
    customer = request.get_json()

    try:
      new_customer = Customer(
        name=customer['name']
      )
      new_customer.insert()

      return jsonify({
        'success': True,
        'customer': new_customer.format()
      })

    except Exception as e:
      abort(422)
  
  @app.route('/orders', methods=['POST'])
  def create_order():
    order = request.get_json()

    try:
      new_order = Order(
        customer=order['customer'],
        value=order['value'],
        date=order['date']
      )
      new_order.insert()

      return jsonify({
        'success': True,
        'order': new_order.format()
      })
    
    except Exception as e:
      abort(422)
  
  @app.route('/deliveries', methods=['POST'])
  def create_delivery():
    delivery = request.get_json()

    try:
      new_delivery = Delivery(
        order=delivery['order'],
        delivery_date=['delivery_date']
      )
      new_delivery.insert()

      return jsonify({
        'success': True,
        'delivery': new_delivery.format()
      })
    
    except Exception as e:
      abort(422)

  @app.route('/customers/<customer_id>', methods=['PATCH'])
  def update_customer(customer_id):
    

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)