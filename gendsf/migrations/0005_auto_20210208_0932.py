# Generated by Django 3.1 on 2021-02-08 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gendsf', '0004_auto_20201224_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='DADSFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ficheVersementSpontaneIRPP', models.FileField(null=True, upload_to='versements/')),
            ],
        ),
        migrations.CreateModel(
            name='DSFFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ficheVersementTVA', models.FileField(null=True, upload_to='tva/')),
                ('ficheVersementAccompteIS', models.FileField(null=True, upload_to='is/')),
                ('balanceSixColonneSYSCohada', models.FileField(null=True, upload_to='syscohoda/')),
                ('personnelPropre', models.FileField(null=True, upload_to='ficheeffectif/')),
                ('personnelExterieur', models.FileField(null=True, upload_to='ficheeffectif/')),
            ],
        ),
        migrations.RemoveField(
            model_name='dads',
            name='ficheVersementSpontaneIRPP',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='balanceSixColonneSYSCohada',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='ficheVersementAccompteIS',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='ficheVersementTVA',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='informationsAutres',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='personnelExterieur',
        ),
        migrations.RemoveField(
            model_name='dsf',
            name='personnelPropre',
        ),
        migrations.AddField(
            model_name='dads',
            name='dadsFile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gendsf.dadsfile'),
        ),
        migrations.AddField(
            model_name='dsf',
            name='dsfFile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gendsf.dsffile'),
        ),
    ]