# Generated by Django 3.1 on 2021-03-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0003_auto_20210210_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarifdouanier',
            name='ts',
            field=models.IntegerField(default=0),
        ),
    ]
