# Generated by Django 3.2.25 on 2024-04-05 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_auto_20240405_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayRequest',
            fields=[
                ('moneytransfer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payapp.moneytransfer')),
            ],
            bases=('payapp.moneytransfer',),
        ),
    ]
