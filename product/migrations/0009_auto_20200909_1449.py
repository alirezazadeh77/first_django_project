# Generated by Django 3.1 on 2020-09-09 14:49

from django.db import migrations, models
import product.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_screenes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=product.models.save_dir),
        ),
    ]
