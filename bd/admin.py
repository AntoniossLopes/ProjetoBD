from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Jogador, Campo, Equipa, Jogo, Torneio, Profile


class JogadorAdmin(admin.ModelAdmin):
    fields = ['user_cc', 'saldo', 'numFalhasJogos','capitao'
        , 'reserva', 'posicao', 'equipa', 'suplente','titular']


class EquipaAdmin(admin.ModelAdmin):
    fields = ['nome', 'emtorneio', 'numGuardaRedes','numGuardaRedesSuplentes','numDefesas', 'numMedios', 'numAvancados'
        , 'numDefesasSuplentes', 'numMediosSuplentes', 'numAvancadosSuplentes','DefesasTatica','MediosTatica','AvancadosTatica',
              'torneio', 'numTotalJogadores']


class CampoAdmin(admin.ModelAdmin):
    fields = ['nome', 'localizacao', 'preco']


class ProfileAdmin(admin.ModelAdmin):
    fields = ['username','estado', 'email', 'first_name', 'last_name', 'cc', 'contacto', 'admin', 'gestor_torneio', 'password']


admin.site.register(Torneio)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Jogo)
admin.site.register(Jogador, JogadorAdmin)
admin.site.register(Equipa, EquipaAdmin)
admin.site.register(Campo, CampoAdmin)
