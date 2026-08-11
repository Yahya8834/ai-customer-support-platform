from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "documents_processing",
            "0002_documentchunk",
        ),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE EXTENSION IF NOT EXISTS vector;
            """,
            reverse_sql="""
                DROP EXTENSION IF EXISTS vector;
            """,
        ),
    ]