# Generated by Django 3.1 on 2020-11-13 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionlicence', '0008_auto_20201113_0555'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestionlicence.application'),
            preserve_default=False,
        ),
    ]
