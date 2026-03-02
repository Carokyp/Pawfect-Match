# Generated manually to fix profile_photo null constraint

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_ownerprofile_completed'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE profiles_ownerprofile ALTER COLUMN profile_photo DROP NOT NULL;',
            reverse_sql='ALTER TABLE profiles_ownerprofile ALTER COLUMN profile_photo SET NOT NULL;'
        ),
    ]
