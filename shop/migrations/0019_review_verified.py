# Generated by Django 3.0.5 on 2020-07-17 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
