# Generated by Django 5.1 on 2024-08-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_rename_shpped_order_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]