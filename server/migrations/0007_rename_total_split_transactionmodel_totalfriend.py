# Generated by Django 4.1.4 on 2023-01-04 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_alter_transactionmodel_total_split'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionmodel',
            old_name='total_split',
            new_name='totalfriend',
        ),
    ]
