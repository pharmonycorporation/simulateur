# Generated by Django 3.1 on 2021-03-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0011_auto_20210315_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pays',
            name='code',
            field=models.CharField(max_length=255),
        ),
    ]