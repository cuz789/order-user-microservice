import pika
import json
import os

def send_update_event(user_id, email, delivery_address):
    # Get RabbitMQ connection details from environment variables
    rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
    rabbitmq_password = os.getenv("RABBITMQ_DEFAULT_PASS")

    # Set up credentials
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=credentials
    ))
    channel = connection.channel()

    # Declare the exchange and set type to fanout
    channel.exchange_declare(exchange='user_updates', exchange_type='fanout')

    # Message payload
    message = {
        "user_id": user_id,
        "email": email,
        "delivery_address": delivery_address
    }
    channel.basic_publish(
        exchange='user_updates',
        routing_key='',
        body=json.dumps(message)
    )

    connection.close()
