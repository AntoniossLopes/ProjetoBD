import datetime

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from bd.models import Profile, Equipa, Torneio, Jogador, Jogo, Campo, Notificacao

POSICOES_JOGADOR = [
    ("defesa", "Defesa"),
    ("medio", "Medio"),
    ("avancado", "Avancado"),
    ("guarda-redes", "Guarda-Rede"),
]


class SignUpForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'cc', 'contacto', 'password1', 'password2')


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name', 'last_name', 'contacto', 'password',)


class LoginForm(AuthenticationForm):
    class Meta:
        model = Profile
        fields = ('username', 'password',)


class PermissoesForm(forms.ModelForm):
    gestor_torneio = forms.CharField()

    class Meta:
        model = Profile
        fields = ('email',)


class CreateTeamForm(forms.ModelForm):
    nome = forms.CharField()

    class Meta:
        model = Equipa
        fields = ('nome', 'emtorneio', 'torneio', 'DefesasTatica', 'MediosTatica', 'AvancadosTatica')
        widgets = {'emtorneio': forms.HiddenInput(), 'torneio': forms.HiddenInput()}


class CreatePlayerForm(forms.ModelForm):
    posicao = forms.TextInput()
    saldo = forms.IntegerField()

    class Meta:
        model = Jogador
        fields = ('posicao', 'saldo', 'equipa', 'user_cc', 'reserva',)
        widgets = {'user_cc': forms.HiddenInput(), 'reserva': forms.HiddenInput()
            , "posicao": forms.Select(choices=POSICOES_JOGADOR)}


class CreateTournamentForm(forms.ModelForm):
    nome = forms.CharField()
    dataInicio = forms.DateField()
    diasJogo = forms.TextInput()
    horarioInicio = forms.TimeField()

    class Meta:
        model = Torneio
        fields = ('nome', 'dataInicio', 'diasJogo', 'horarioInicio', 'gestor')


class AddCaptainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.team_name = kwargs.pop('team_name')
        super(AddCaptainForm, self).__init__(*args, **kwargs)
        self.fields['jogadores'] = forms.ModelChoiceField(queryset=Jogador.objects.filter(equipa=self.team_name))

    jogadores = forms.TextInput()


class FaltasPagamentosForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.team_name = kwargs.pop('team_name')
        super(FaltasPagamentosForm, self).__init__(*args, **kwargs)
        self.fields['jogadores'] = forms.ModelChoiceField(queryset=Jogador.objects.filter(equipa=self.team_name))

    jogadores = forms.TextInput()
    dinheiro = forms.IntegerField()


class FaltasForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.team_name = kwargs.pop('team_name')
        super(FaltasPagamentosForm, self).__init__(*args, **kwargs)
        self.fields['jogadores'] = forms.ModelChoiceField(queryset=Jogador.objects.filter(equipa=self.team_name))

    jogadores = forms.TextInput()
    faltas = forms.IntegerField()


class Resultado(forms.ModelForm):
    resultado1 = forms.IntegerField()
    resultado2 = forms.IntegerField()

    class Meta:
        model = Jogo
        fields = ('resultado1', 'resultado2')


class NotificacaoForm(forms.ModelForm):
    class Meta:
        model = Notificacao
        fields = ('notif', 'pessoa',)


