# Generated by Django 3.1 on 2021-02-10 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarifdouanier',
            name='quotite',
            field=models.IntegerField(default=0),
        ),
    ]
