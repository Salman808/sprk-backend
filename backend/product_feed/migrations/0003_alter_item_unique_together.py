# Generated by Django 4.2 on 2023-05-06 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_feed', '0002_alter_item_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('code', 'type')},
        ),
    ]
