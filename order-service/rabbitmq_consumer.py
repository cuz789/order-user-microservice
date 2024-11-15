import pika
import json
import os
import time
from pymongo import MongoClient

# Connect to MongoDB using environment variable
client = MongoClient(os.getenv("MONGO_URI"))
db = client.order_management
order_collection = db.orders

def callback(ch, method, properties, body):
    message = json.loads(body)
    user_id = message["user_id"]
    email = message["email"]
    delivery_address = message["delivery_address"]

    # Update all orders for the user with the new email and address
    order_collection.update_many(
        {"user_id": user_id},
        {"$set": {"email": email, "delivery_address": delivery_address}}
    )
    print(f"Updated orders for user_id {user_id}")

def start_consumer():
    # Add a delay to allow RabbitMQ to fully initialize
    time.sleep(10)

    # Get RabbitMQ connection details from environment variables
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
    rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")

    # Set up credentials
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
    )
    channel = connection.channel()

    # Declare the exchange and create an exclusive queue for this consumer
    channel.exchange_declare(exchange='user_updates', exchange_type='fanout')
    queue_name = channel.queue_declare(queue='', exclusive=True).method.queue
    channel.queue_bind(exchange='user_updates', queue=queue_name)

    # Consume messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("Waiting for messages...")
    channel.start_consuming()
