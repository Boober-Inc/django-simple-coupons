# Generated by Django 3.1.1 on 2021-01-26 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_coupons', '0003_add_description_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='CouponUser',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]
