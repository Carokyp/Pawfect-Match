# Generated manually to fix profile_photo null constraint

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0008_dog_completed'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE dogs_dog ALTER COLUMN profile_photo DROP NOT NULL;',
            reverse_sql='ALTER TABLE dogs_dog ALTER COLUMN profile_photo SET NOT NULL;'
        ),
    ]
