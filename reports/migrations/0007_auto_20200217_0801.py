# Generated by Django 2.1.15 on 2020-02-17 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20200109_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=500, verbose_name='Область')),
                ('emails', models.CharField(max_length=1500, blank=True, null=True, verbose_name='Адреса почт координаторов')),
                ('is_draft', models.BooleanField(default=True, verbose_name='Черновик')),
            ],
            options={
                'verbose_name': 'Подключенная область',
                'verbose_name_plural': 'Подключенные области',
            },
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together={('id', 'state_name')},
        ),
    ]
