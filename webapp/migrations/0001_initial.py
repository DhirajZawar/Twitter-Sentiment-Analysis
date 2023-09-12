# Generated by Django 4.0.5 on 2022-06-25 15:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2022, 6, 25, 15, 44, 48, 338589, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet', models.TextField()),
                ('polarity', models.CharField(max_length=20)),
                ('subjectivity', models.CharField(max_length=20)),
                ('query_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webapp.searchquery')),
            ],
        ),
    ]
