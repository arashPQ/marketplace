# Generated by Django 5.1 on 2024-10-13 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.subcategory'),
        ),
    ]