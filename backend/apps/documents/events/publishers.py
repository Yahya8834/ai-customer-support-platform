import json
import pika
from dataclasses import asdict
from apps.documents.events.contracts import DocumentUploadedEvent
from apps.common.rabbitmq import get_connection
from apps.documents.events.constants import (
    DOCUMENTS_EXCHANGE,
    DOCUMENT_UPLOADED_ROUTING_KEY,
)



def publish_document_uploaded(event: DocumentUploadedEvent) -> None:
    """
    Publish a DocumentUploadedEvent to RabbitMQ.
    """

    connection = get_connection()

    try:
        channel = connection.channel()

        channel.exchange_declare(
            exchange=DOCUMENTS_EXCHANGE,
            exchange_type="topic",
            durable=True,
        )

        channel.basic_publish(
            exchange=DOCUMENTS_EXCHANGE,
            routing_key=DOCUMENT_UPLOADED_ROUTING_KEY,
            body=json.dumps(asdict(event), default=str),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )

    finally:
        connection.close()