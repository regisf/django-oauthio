# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthioUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(help_text='From which Social network the user comes', max_length=20, verbose_name='Provider')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL, help_text='The django framework username')),
            ],
        ),
    ]
