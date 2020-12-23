# Generated by Django 3.1 on 2020-12-23 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gendsf', '0002_remove_fichefiscale_sigleusuel'),
    ]

    operations = [
        migrations.AddField(
            model_name='identification',
            name='nombreEts',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='identification',
            name='pays',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gendsf.pays'),
        ),
    ]
