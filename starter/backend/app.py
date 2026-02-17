from os import abort

from flask import Flask, request, jsonify, send_from_directory

from backend.exception.duplicate_order_error import DuplicateOrderError
from backend.exception.empty_order_id_error import EmptyOrderIdError
from backend.exception.invalid_initial_status_error import InvalidInitialStatusError
from backend.exception.minimum_order_quantity_error import MinimumOrderQuantityError
from backend.exception.order_not_found_error import OrderNotFoundError
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    # DONE (1): Add new order
    new_order = dict(request.json)
    try:
        order = order_tracker.add_order(**new_order)

        return jsonify(order), 201
    except (MinimumOrderQuantityError, InvalidInitialStatusError) as e:
        return { "error": e.message }, 400
    except DuplicateOrderError as e:
        return { "error": e.message }, 409

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    # DONE (2): Get order details by ID
    try:
        order = order_tracker.get_order_by_id(order_id)
        if not order:
            return { "error": "Not found" }, 404
        return jsonify(order), 200
    except EmptyOrderIdError as e:
        return { "error": e.MESSAGE }, 400

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    # DONE (3): Update order status
    new_status = dict(request.json)
    try:
        order = order_tracker.update_order_status(order_id, new_status.get("new_status"))
        return jsonify(order), 200
    except EmptyOrderIdError as e:
        return { "error": e.MESSAGE }, 400
    except InvalidInitialStatusError as e:
        return { "error": e.message }, 400
    except OrderNotFoundError as e:
        return { "error": e.message }, 404

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    # DONE (4): List all orders
    # TODO (5): Filter orders by status
    orders = order_tracker.list_all_orders()
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
