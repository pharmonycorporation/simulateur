# Generated by Django 3.0.3 on 2020-11-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionlicence', '0006_auto_20201112_1905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='licence',
            name='firstConnect',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='licence',
            name='user_nbre',
            field=models.IntegerField(default=0),
        ),
    ]