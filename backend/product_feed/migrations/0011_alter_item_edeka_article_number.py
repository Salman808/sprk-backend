# Generated by Django 4.2 on 2023-05-07 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_feed', '0010_item_edeka_article_number_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='edeka_article_number',
            field=models.JSONField(blank=True, max_length=255, null=True),
        ),
    ]
