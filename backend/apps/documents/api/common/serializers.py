from rest_framework import serializers
from apps.documents.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "uuid",
            "original_filename",
            "content_type",
            "file_size",
            "processing_status",
            "uploaded_at",
        )