# Generated by Django 3.1 on 2020-09-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commenting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcomment',
            name='approved_time',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
