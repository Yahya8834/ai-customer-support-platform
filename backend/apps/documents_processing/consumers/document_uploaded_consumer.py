import json
from apps.common.rabbitmq import get_connection
from apps.documents.models import Document
from apps.documents_processing.services.process_document import ProcessDocumentService
from apps.documents.events.constants import (
    DOCUMENTS_EXCHANGE,
    DOCUMENTS_PROCESSING_QUEUE,
    DOCUMENT_UPLOADED_ROUTING_KEY,
)



def start_consumer() -> None:
    connection = get_connection()

    channel = connection.channel()

    channel.exchange_declare(
        exchange=DOCUMENTS_EXCHANGE,
        exchange_type="topic",
        durable=True,
    )

    channel.queue_declare(
        queue=DOCUMENTS_PROCESSING_QUEUE,
        durable=True,
    )

    channel.queue_bind(
        exchange=DOCUMENTS_EXCHANGE,
        queue=DOCUMENTS_PROCESSING_QUEUE,
        routing_key=DOCUMENT_UPLOADED_ROUTING_KEY,
    )

    channel.basic_consume(
        queue=DOCUMENTS_PROCESSING_QUEUE,
        on_message_callback=on_document_uploaded,
    )


    channel.start_consuming()




def on_document_uploaded(channel, method, properties, body):
    event = json.loads(body)


    try:
        ProcessDocumentService.execute(
            document_uuid=event["document_uuid"],
        )

    except Exception as exc:
        document = Document.objects.get(
            uuid=event["document_uuid"],
        )

        document.processing_status = (
            Document.ProcessingStatus.FAILED
        )

        document.save(
            update_fields=[
                "processing_status",
            ]
        )


    finally:
        channel.basic_ack(
            delivery_tag=method.delivery_tag,
        )