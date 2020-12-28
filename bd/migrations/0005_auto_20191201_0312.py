# Generated by Django 2.0.5 on 2019-12-01 03:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0004_auto_20191130_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jogador',
            old_name='numFalhasJogo',
            new_name='numFalhasJogos',
        ),
        migrations.AlterField(
            model_name='jogo',
            name='equipaAGolos',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='jogo',
            name='equipaBGolos',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='notificacao',
            name='pessoa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
