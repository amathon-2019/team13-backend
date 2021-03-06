# Generated by Django 2.2.4 on 2019-08-31 10:25

import apps.user.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='키')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화 여부')),
                ('expired', models.DateTimeField(default=apps.user.models.default_token_expire, verbose_name='만료일')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
            options={
                'verbose_name': '토큰',
                'verbose_name_plural': '토큰 목록',
                'db_table': 'token',
            },
        ),
    ]
