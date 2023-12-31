# Generated by Django 4.2.6 on 2023-10-26 05:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mblogapp', '0002_category_profile_phone_no_blogpost_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0),
        ),
    ]
