# Generated by Django 4.2.6 on 2023-11-01 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mblogapp', '0005_alter_blogpost_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]