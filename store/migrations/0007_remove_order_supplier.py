# Generated by Django 3.1.12 on 2022-02-02 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20220201_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='supplier',
        ),
    ]