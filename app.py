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
    customer = request.get_json()

    try:
      customer_db = Customer.query.filter(Customer.id==int(customer_id)).one_or_none()

      if customer_db is None:
        abort(404)
      
      if 'name' in customer:
        customer_db.name = customer['name']
        customer_db.update()
      
      return jsonify({
        'success': True,
        'customer': customer_db.format()
      })
    
    except BaseException as e:
      abort(422)
  
  @app.route('/orders/<order_id>', methods=['PATCH'])
  def update_order(order_id):
    order = request.get_json()

    try:
      order_db = Order.query.filter(Order.id==int(order_id)).one_or_none()

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
    
    except BaseException as e:
      abort(422)
  


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)