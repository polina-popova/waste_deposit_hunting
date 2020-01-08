# Generated by Django 2.2.8 on 2020-01-06 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20200104_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentComplain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('datetime_received', models.DateTimeField(auto_now=True, verbose_name='Дата получения жалобы на контент')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report', verbose_name='Сообщение о свалке')),
            ],
        ),
    ]
