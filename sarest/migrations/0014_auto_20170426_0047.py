# Generated by Django 2.0.dev20170411164641 on 2017-04-26 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sarest', '0013_auto_20170426_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='sarest.Category'),
        ),
        migrations.AlterField(
            model_name='userbooks',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='book', to='sarest.Book'),
        ),
        migrations.AlterField(
            model_name='userbooks',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
