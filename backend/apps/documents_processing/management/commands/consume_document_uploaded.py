from django.core.management.base import BaseCommand
from apps.documents_processing.consumers.document_uploaded_consumer import (
    start_consumer,
)


class Command(BaseCommand):
    help = "Start the Document Uploaded RabbitMQ consumer."

    def handle(self, *args, **options):
        start_consumer()