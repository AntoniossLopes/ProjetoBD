from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from datetime import *
from dateutil.relativedelta import *
import calendar
import pytz
# Create your models here.
from django.dispatch import receiver

class Profile(AbstractUser):
    cc = models.IntegerField(blank=False, primary_key=True)
    contacto = models.IntegerField(blank=False, default='0')
    admin = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)  #confirmed ou nao
    gestor_torneio = models.BooleanField(default=False)


class Torneio(models.Model):
    nome = models.CharField(max_length=20, blank=False)
    dataInicio = models.DateField(blank=False)
    diasJogo = models.TextField(blank=True)
    horarioInicio = models.TimeField(blank=True)
    gestor = models.ForeignKey(Profile, blank=False, on_delete=models.CASCADE)
    estado = models.IntegerField(default='0') #0:inscricoes abertas ; 1:a decorrer ; 2:terminado


class Equipa(models.Model):
    nome = models.CharField(max_length=20, blank=False, primary_key=True)
    numTotalJogadores = models.IntegerField(default='0')
    emtorneio = models.BooleanField()

    DefesasTatica = models.IntegerField(blank=False,default='0')
    MediosTatica = models.IntegerField(blank=False,default='0')
    AvancadosTatica = models.IntegerField(blank=False,default='0')


    numGuardaRedes = models.IntegerField(default='0')
    numGuardaRedesSuplentes = models.IntegerField(default='0')
    numDefesas = models.IntegerField(default='0')
    numMedios = models.IntegerField(default='0')
    numAvancados = models.IntegerField(default='0')
    numDefesasSuplentes = models.IntegerField(default='0')
    numMediosSuplentes = models.IntegerField(default='0')
    numAvancadosSuplentes = models.IntegerField(default='0')
    torneio = models.ForeignKey(Torneio, blank=False, on_delete=models.CASCADE)

    pontos = models.IntegerField(blank=False, default='0')
    vitorias = models.IntegerField(blank=False, default='0')
    empates = models.IntegerField(blank=False, default='0')
    derrotas = models.IntegerField(blank=False, default='0')
    golosMarcados = models.IntegerField(blank=False, default='0')
    golosSofridos = models.IntegerField(blank=False, default='0')

    def __str__(self):
        return self.nome


class Jogador(models.Model):
    user_cc = models.ForeignKey(Profile, on_delete=models.CASCADE)
    saldo = models.IntegerField(default='0')
    numFalhasJogos = models.IntegerField(blank=True, default='0')

    titular = models.BooleanField(default=False)
    suplente = models.BooleanField(default=False)
    reserva = models.BooleanField(blank=True, default=False)

    posicao = models.TextField(blank=False)
    capitao = models.BooleanField(default=False)
    equipa = models.ForeignKey(Equipa, on_delete=models.CASCADE)
    numFalhasPagamento = models.IntegerField(default='0')
    pagamentosCompletos = models.IntegerField(default='0')
    golos = models.IntegerField(blank=False, default='0')

    def __str__(self):
        return self.user_cc.first_name


class Campo(models.Model):
    nome = models.CharField(max_length=20, blank=False)
    localizacao = models.TextField(blank=False)
    preco = models.IntegerField(blank=True)

    def __str__(self):
        return self.nome

class Jogo(models.Model):
    equipaAGolos = models.IntegerField(default= -1)
    equipaBGolos = models.IntegerField(default= -1)
    equipa1 = models.ForeignKey(Equipa, blank=False, on_delete=models.CASCADE, related_name= 'jogos')
    equipa2 = models.ForeignKey(Equipa, blank=False, on_delete=models.CASCADE, related_name= 'equipa2' )
    torneio = models.ForeignKey(Torneio, blank=False, on_delete=models.CASCADE)
    campo = models.ForeignKey(Campo, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return "A Golos:" + str(self.equipaAGolos) + " vs B Golos: " + str(self.equipaBGolos)


class Notificacao(models.Model):
    notif = models.TextField(blank=False)
    pessoa = models.ForeignKey(Profile, blank=False, on_delete=models.CASCADE, null=True)