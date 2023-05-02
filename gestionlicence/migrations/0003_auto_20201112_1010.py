# Generated by Django 3.1 on 2020-11-12 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionlicence', '0002_auto_20201112_0633'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyPackages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_souscription', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionlicence.package')),
                ('personne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestionlicence.personne')),
            ],
        ),
        migrations.AddField(
            model_name='personne',
            name='packages',
            field=models.ManyToManyField(related_name='personnes', through='gestionlicence.MyPackages', to='gestionlicence.Package'),
        ),
    ]
