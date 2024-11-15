from flask import Flask, request, jsonify
from pymongo import MongoClient
from rabbitmq_producer import send_update_event
import os

app = Flask(__name__)

# Connect to MongoDB Atlas using environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client.order_management
user_collection = db.users

# Endpoint to create a new user
@app.route('/v1/users', methods=['POST'])
def create_user():
    data = request.json
    user = {
        "user_id": data.get("user_id"),
        "name": data.get("name"),
        "email": data.get("email"),
        "delivery_address": data.get("delivery_address")
    }
    result = user_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return jsonify({"message": "User created successfully", "user": user}), 201

# Endpoint to update a user's email or delivery address
@app.route('/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    update_fields = {}
    if "email" in data:
        update_fields["email"] = data["email"]
    if "delivery_address" in data:
        update_fields["delivery_address"] = data["delivery_address"]

    result = user_collection.update_one({"user_id": user_id}, {"$set": update_fields})
    if result.matched_count > 0:
        # Send update event to RabbitMQ
        send_update_event(user_id, data.get("email"), data.get("delivery_address"))
        return jsonify({"message": "User updated successfully", "user_id": user_id}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Endpoint to get a user's details by user_id
@app.route('/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_collection.find_one({"user_id": user_id})
    if user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON serialization
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
