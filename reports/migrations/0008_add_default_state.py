from django.db import migrations

from reports.models import State


DEFAULT_STATE_NAME = 'Архангельская область'


def create_default_state(apps, schema_editor):
    State.objects.get_or_create(state_name=DEFAULT_STATE_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_auto_20200217_0801'),
    ]

    operations = [
        migrations.RunPython(create_default_state),
    ]
