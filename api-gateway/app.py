import os
import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Base URLs for microservices
USER_SERVICE_V1_URL = os.getenv("USER_SERVICE_V1_URL", "http://user-service-v1:5000/v1/users")
USER_SERVICE_V2_URL = os.getenv("USER_SERVICE_V2_URL", "http://user-service-v2:5001/v2/users")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:5002/orders")

# Set the traffic ratio for v2
P_RATIO = float(os.getenv("P_RATIO", 0.5))  # Default to 50% traffic for v2

# Helper function to decide which version of user service to use
def route_to_user_service():
    random_value = random.random()  # Generate a random number
    print(f"Generated random value: {random_value}", flush=True) 
    if random_value < P_RATIO:
        print("Routing to USER_SERVICE_V2_URL", flush=True)
        return USER_SERVICE_V2_URL
    else:
        print("Routing to USER_SERVICE_V1_URL", flush=True)
        return USER_SERVICE_V1_URL

# API Gateway endpoints

# Route to get user details
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    url = f"{route_to_user_service()}/{user_id}"
    response = requests.get(url)
    return jsonify(response.json()), response.status_code

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    url = route_to_user_service()
    response = requests.post(url, json=request.json)
    return jsonify(response.json()), response.status_code

# Route to update user details
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    url = f"{route_to_user_service()}/{user_id}"
    response = requests.put(url, json=request.json)
    return jsonify(response.json()), response.status_code

# Route to handle order-related requests
@app.route('/orders/<status>', methods=['GET'])
def get_order(status):
    url = f"{ORDER_SERVICE_URL}/{status}"
    response = requests.get(url)
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['POST'])
def create_order():
    response = requests.post(ORDER_SERVICE_URL, json=request.json)
    return jsonify(response.json()), response.status_code

# Route to update order details
@app.route('/orders/<order_id>/status', methods=['PUT'])
def update_order(order_id):
    url = f"{ORDER_SERVICE_URL}/{order_id}/status"
    response = requests.put(url, json=request.json)
    return jsonify(response.json()), response.status_code

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
