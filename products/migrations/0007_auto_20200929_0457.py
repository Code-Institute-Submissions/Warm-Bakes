# Generated by Django 2.2.13 on 2020-09-28 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200929_0258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='cover',
        ),
    ]