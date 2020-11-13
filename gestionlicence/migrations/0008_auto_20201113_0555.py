# Generated by Django 3.1 on 2020-11-13 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionlicence', '0007_auto_20201112_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypackages',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='licence',
            name='pack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licence', to='gestionlicence.package'),
        ),
    ]
