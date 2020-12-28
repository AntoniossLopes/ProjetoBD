# Generated by Django 2.0.5 on 2019-11-30 16:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cc', models.IntegerField(primary_key=True, serialize=False)),
                ('contacto', models.IntegerField(default='0')),
                ('admin', models.BooleanField(default=False)),
                ('estado', models.BooleanField(default=True)),
                ('gestor_torneio', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('localizacao', models.TextField()),
                ('preco', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipa',
            fields=[
                ('nome', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('numTotalJogadores', models.IntegerField(default='0')),
                ('emtorneio', models.BooleanField()),
                ('DefesasTatica', models.IntegerField(default='0')),
                ('MediosTatica', models.IntegerField(default='0')),
                ('AvancadosTatica', models.IntegerField(default='0')),
                ('numGuardaRedes', models.IntegerField(default='0')),
                ('numGuardaRedesSuplentes', models.IntegerField(default='0')),
                ('numDefesas', models.IntegerField(default='0')),
                ('numMedios', models.IntegerField(default='0')),
                ('numAvancados', models.IntegerField(default='0')),
                ('numDefesasSuplentes', models.IntegerField(default='0')),
                ('numMediosSuplentes', models.IntegerField(default='0')),
                ('numAvancadosSuplentes', models.IntegerField(default='0')),
                ('pontos', models.IntegerField(default='0')),
                ('vitorias', models.IntegerField(default='0')),
                ('empates', models.IntegerField(default='0')),
                ('derrotas', models.IntegerField(default='0')),
                ('golosMarcados', models.IntegerField(default='0')),
                ('golosSofridos', models.IntegerField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Jogador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.IntegerField(default='0')),
                ('numFalhasJogos', models.IntegerField(blank=True, default='0')),
                ('titular', models.BooleanField(default=False)),
                ('suplente', models.BooleanField(default=False)),
                ('reserva', models.BooleanField(default=False)),
                ('posicao', models.TextField()),
                ('capitao', models.BooleanField(default=False)),
                ('numFalhasPagamento', models.IntegerField(default='0')),
                ('pagamentosCompletos', models.IntegerField(default='0')),
                ('golos', models.IntegerField(default='0')),
                ('equipa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.Equipa')),
                ('user_cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Jogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipaAGolos', models.IntegerField(default=0)),
                ('equipaBGolos', models.IntegerField(default=0)),
                ('date', models.DateTimeField()),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.Campo')),
                ('equipa1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jogos', to='bd.Equipa')),
                ('equipa2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipa2', to='bd.Equipa')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif', models.TextField()),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Torneio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('dataInicio', models.DateField()),
                ('diasJogo', models.TextField(blank=True)),
                ('horarioInicio', models.TimeField(blank=True)),
                ('gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='jogo',
            name='torneio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.Torneio'),
        ),
        migrations.AddField(
            model_name='equipa',
            name='torneio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.Torneio'),
        ),
    ]
