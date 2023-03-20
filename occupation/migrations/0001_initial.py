# Generated by Django 4.1.5 on 2023-03-20 12:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '__first__'),
        ('houses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('rent_due_date', models.DateField(blank=True, null=True)),
                ('rent_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('occupied', models.BooleanField(default=True)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.house')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('occupation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='occupation.occupation')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trial', to='tenant.tenant')),
            ],
        ),
    ]
