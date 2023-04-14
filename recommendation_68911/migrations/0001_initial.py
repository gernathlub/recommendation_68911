from django.db import migrations

class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql=["CREATE EXTENSION IF NOT EXISTS cube"],
            reverse_sql=["DROP EXTENSION IF EXISTS cube"],
        ),
    ]