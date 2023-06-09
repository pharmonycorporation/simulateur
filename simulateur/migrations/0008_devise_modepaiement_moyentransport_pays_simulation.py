# Generated by Django 3.1 on 2021-03-15 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simulateur', '0007_auto_20210309_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomDevise', models.CharField(max_length=255)),
                ('codeDevise', models.CharField(max_length=255)),
                ('numeroDevise', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ModePaiement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoyenTransport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moyen', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('cemac', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('tva', models.FloatField(default=18)),
            ],
        ),
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importateur', models.CharField(max_length=255, verbose_name='Raison sociale')),
                ('regimeFiscale', models.CharField(max_length=255)),
                ('nomenclature', models.CharField(max_length=255)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivee', to='simulateur.pays')),
                ('devise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulateur.devise')),
                ('modePaiement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulateur.modepaiement')),
                ('moyenTransport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulateur.moyentransport')),
                ('origine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='depart', to='simulateur.pays')),
            ],
        ),
    ]
