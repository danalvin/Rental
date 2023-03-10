# Generated by Django 4.1.5 on 2023-02-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='house',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('housenumber', models.PositiveIntegerField(unique=True)),
                ('tenant', models.CharField(max_length=150)),
                ('Water', models.PositiveIntegerField()),
                ('internet_subscription', models.PositiveIntegerField()),
                ('rent', models.PositiveIntegerField()),
            ],
        ),
    ]
