# Generated by Django 3.0.5 on 2020-06-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200608_1911'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='clothing_type',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, max_length=65, null=True, unique=True),
        ),
    ]