from flask import Flask, request, jsonify
from pymongo import MongoClient
from rabbitmq_consumer import start_consumer
import threading
import os

app = Flask(__name__)

# Connect to MongoDB Atlas using environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client.order_management
order_collection = db.orders

# Run RabbitMQ consumer in a separate thread
threading.Thread(target=start_consumer, daemon=True).start()

# Endpoint to create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = {
        "order_id": data.get("order_id"),
        "user_id": data.get("user_id"),
        "items": data.get("items"),
        "email": data.get("email"),
        "delivery_address": data.get("delivery_address"),
        "status": "under process"  # Default status when an order is created
    }
    result = order_collection.insert_one(order)
    order["_id"] = str(result.inserted_id)
    return jsonify({"message": "Order created successfully", "order": order}), 201

# Endpoint to get orders by status
@app.route('/orders/<status>', methods=['GET'])
def get_orders_by_status(status):
    orders = list(order_collection.find({"status": status}))
    for order in orders:
        order["_id"] = str(order["_id"])  # Convert ObjectId to string for JSON serialization
    return jsonify(orders), 200

# Endpoint to update an order's status
@app.route('/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.json
    status = data.get("status")
    if status not in ["under process", "shipping", "delivered"]:
        return jsonify({"message": "Invalid status"}), 400

    result = order_collection.update_one({"order_id": order_id}, {"$set": {"status": status}})
    if result.matched_count > 0:
        return jsonify({"message": "Order status updated successfully", "order_id": order_id}), 200
    else:
        return jsonify({"message": "Order not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
