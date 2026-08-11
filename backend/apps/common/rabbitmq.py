import os
import pika


def get_connection() -> pika.BlockingConnection:
    """
    Create a connection to RabbitMQ.
    """
    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "rabbitmq"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=pika.PlainCredentials(
            username=os.getenv("RABBITMQ_DEFAULT_USER", "guest"),
            password=os.getenv("RABBITMQ_DEFAULT_PASS", "guest"),
        ),
    )

    return pika.BlockingConnection(parameters)