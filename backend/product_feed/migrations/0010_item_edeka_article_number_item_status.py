# Generated by Django 4.2 on 2023-05-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_feed', '0009_rename_best_before_date_product_bbd_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='edeka_article_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]