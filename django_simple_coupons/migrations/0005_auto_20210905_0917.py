# Generated by Django 3.1.7 on 2021-09-05 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_simple_coupons', '0004_add_created_at_to_coupon_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinPriceRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Min order value')),
            ],
            options={
                'verbose_name': 'Min Price Rule',
                'verbose_name_plural': 'Min Price Rules',
            },
        ),
        migrations.AddField(
            model_name='validityrule',
            name='is_permanent',
            field=models.BooleanField(default=False, verbose_name='Is permanent?'),
        ),
        migrations.AlterField(
            model_name='validityrule',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Expiration date'),
        ),
        migrations.AddField(
            model_name='ruleset',
            name='min_price',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.minpricerule', verbose_name='Min Price rule'),
            preserve_default=False,
        ),
    ]
