# Generated by Django 4.1.4 on 2023-01-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_transactionmodel_total_split_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='total_split',
            field=models.IntegerField(),
        ),
    ]
