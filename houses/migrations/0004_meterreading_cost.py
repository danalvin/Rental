# Generated by Django 4.1.5 on 2023-03-22 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='meterreading',
            name='Cost',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
