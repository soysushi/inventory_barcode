# Generated by Django 3.1.12 on 2022-01-12 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_drop_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='color',
        ),
        migrations.RemoveField(
            model_name='order',
            name='design',
        ),
        migrations.RemoveField(
            model_name='order',
            name='drop',
        ),
    ]
