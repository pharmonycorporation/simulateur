# Generated by Django 3.1 on 2021-03-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0010_auto_20210315_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devise',
            name='codeDevise',
            field=models.CharField(max_length=255),
        ),
    ]
