# Generated by Django 2.2.8 on 2020-01-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20191230_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-pk',), 'verbose_name': 'Отчет', 'verbose_name_plural': 'Отчеты'},
        ),
        migrations.AddField(
            model_name='report',
            name='was_sent',
            field=models.BooleanField(default=False),
        ),
    ]
