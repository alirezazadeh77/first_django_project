# Generated by Django 3.1 on 2020-09-17 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductComment',
        ),
    ]
