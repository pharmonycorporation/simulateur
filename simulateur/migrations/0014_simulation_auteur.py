# Generated by Django 3.1 on 2021-03-17 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionlicence', '0011_auto_20210208_0932'),
        ('simulateur', '0013_auto_20210317_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='auteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionlicence.personne'),
        ),
    ]
