# Generated by Django 2.0.dev20170411164641 on 2017-04-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sarest', '0024_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publish_date',
            field=models.DateField(null=True),
        ),
    ]
