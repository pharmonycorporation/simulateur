# Generated by Django 3.1 on 2021-03-15 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0009_devise_valeurdevise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devise',
            name='codeDevise',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='devise',
            name='nomDevise',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
