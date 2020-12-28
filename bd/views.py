from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from datetime import datetime, timezone
import datetime
from dateutil.relativedelta import *
import calendar
import math
import pytz

from bd.forms import SignUpForm, LoginForm, CreateTeamForm, CreateTournamentForm, ChangeProfileForm, CreatePlayerForm, \
    PermissoesForm, AddCaptainForm, FaltasPagamentosForm, FaltasForm, Resultado, NotificacaoForm
from bd.models import Profile, Torneio, Equipa, Jogador, Jogo, Campo, Notificacao


def home(request):
    data = Torneio.objects.all()

    arg = {
        "torneio_numero": data
    }

    return render(request, "home.html", arg)


def changeProfile_view(request, pk):
    if request.method == 'POST':
        user = Profile.objects.get(pk=pk)
        form = ChangeProfileForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('bd-home')
    else:
        form = ChangeProfileForm()

    return render(request, 'signup.html', {'form': form})


def users_view(request):
    data = Profile.objects.all()

    user = {
        "user_numero": data
    }

    return render(request, 'permissoes.html', user)


def permissoes_view(request, pk):
    if request.method == 'POST':
        user = Profile.objects.get(pk=pk)
        form = PermissoesForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            return redirect('bd-home')
    else:
        form = ChangeProfileForm()

    return render(request, 'signup.html', {'form': form})


def myTeam_view(request, pk):
    global jogador

    try:
        user = Profile.objects.get(pk=pk)

        jogadores_user = Jogador.objects.filter(user_cc=user.cc)

        args = {'pk': pk, 'jogadores_user': jogadores_user}

        return render(request, 'myteam.html', args)
    except Jogador.DoesNotExist:
        return render(request, 'error.html')


def teamMenu_view(request, pk, cc):
    equipa = Equipa.objects.get(pk=pk)
    usuario = Jogador.objects.get(user_cc=cc, equipa=equipa)
    jogadores = Jogador.objects.filter(equipa=equipa)
    jogadoresTitularesGK = jogadores.filter(suplente=False, reserva=False, posicao="guarda-redes")
    jogadoresTitularesDefesas = jogadores.filter(suplente=False, reserva=False, posicao="defesa")
    jogadoresTitularesMedios = jogadores.filter(suplente=False, reserva=False, posicao="medio")
    jogadoresTitularesAvancados = jogadores.filter(suplente=False, reserva=False, posicao="avancado")
    jogadoresSuplentes = jogadores.filter(suplente=True)
    jogadoresReservas = jogadores.filter(reserva=True)

    args = {'pk': pk, 'cc': cc, 'equipa': equipa, "jogadoresTitularesGK": jogadoresTitularesGK,
            'jogadoresTitularesDefesas': jogadoresTitularesDefesas,
            "jogadoresTitularesMedios": jogadoresTitularesMedios,
            "jogadoresTitularesAvancados": jogadoresTitularesAvancados,
            "jogadoresSuplentes": jogadoresSuplentes, "jogadoresReservas": jogadoresReservas,
            'usuario': usuario}

    return render(request, "teamMenu.html", args)


def faltasAtraso_view(request, pk, cc):
    if request.method == 'POST':
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = FaltasPagamentosForm(request.POST, team_name=equipa.nome)
        args = {'pk': pk, 'cc': cc, 'equipa': equipa, 'jogadores': jogadores, 'form': form}
        if form.is_valid():
            username = form.cleaned_data.get('jogadores')
            opcoes = request.POST.getlist("tipo")
            dinheiro = form.cleaned_data.get('dinheiro')
            user_jogador = Profile.objects.get(first_name=username)
            jogador = Jogador.objects.get(user_cc=user_jogador.cc)

            if opcoes == "adicionar saldo":
                jogador.saldo = jogador.saldo + dinheiro
                jogador.save()
                return render(request, 'registaAtraso.html', args)
            if opcoes == "pagar atraso":
                jogador.saldo = jogador.saldo - dinheiro
                jogador.pagamentosCompletos = jogador.pagamentosCompletos + 1
                jogador.save()
                return render(request, 'registaAtraso.html', args)
    else:
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = FaltasPagamentosForm(team_name=equipa.nome)
        args = {'pk': pk, 'cc': cc, 'equipa': equipa, 'jogadores': jogadores, 'form': form}

    return render(request, 'registaAtraso.html', args)


def faltasPagamentos_view(request, pk, cc):
    if request.method == 'POST':
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = FaltasPagamentosForm(request.POST, team_name=equipa.nome)
        args = {'pk': pk, 'cc': cc, 'equipa': equipa, 'jogadores': jogadores, 'form': form}
        if form.is_valid():
            username = form.cleaned_data.get('jogadores')
            opcoes = request.POST.getlist("tipo")
            inteiro = form.cleaned_data.get('faltas')
            user_jogador = Profile.objects.get(first_name=username)
            jogador = Jogador.objects.get(user_cc=user_jogador.cc)

            if opcoes == "adicionar jogo":
                jogador.numFalhasJogos = jogador.numFalhasJogos + 1
                jogador.save()
                return render(request, 'faltasPagamentos.html', args)
            if opcoes == "falta pagamento":
                jogador.numFalhasPagamento = jogador.numFalhasPagamento + 1
                jogador.save()
                return render(request, 'faltasPagamentos.html', args)
    else:
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = FaltasPagamentosForm(team_name=equipa.nome)
        args = {'pk': pk, 'cc': cc, 'equipa': equipa, 'jogadores': jogadores, 'form': form}

    return render(request, 'faltasPagamentos.html', args)


def jogador_view(request, pk, cc, ccplayer):
    jogadores = Jogador.objects.filter(equipa=pk)
    for x in jogadores:
        if (x.user_cc.cc == ccplayer):
            jogador = x
            args = {"pk": pk, "cc": cc, "ccplayer": ccplayer, "jogador": jogador}
            return render(request, "playerinfo.html", args)

    return render(request, "error.html")


def jogadortour_view(request, pk, cc, ccplayer, ver0):
    jogadores = Jogador.objects.filter(equipa=pk)
    for x in jogadores:
        if (x.user_cc.cc == ccplayer):
            jogador = x
            args = {"pk": pk, "cc": cc, "ccplayer": ccplayer, "jogador": jogador, "ver0": ver0}
            return render(request, "playertour.html", args)

    return render(request, "error.html")


def jogadorguest_view(request, pk, ccplayer):
    jogadores = Jogador.objects.filter(equipa=pk)
    for x in jogadores:
        if (x.user_cc.cc == ccplayer):
            jogador = x
            args = {"pk": pk, "ccplayer": ccplayer, "jogador": jogador}
            return render(request, "playerinfoguest.html", args)

    return render(request, "error.html")


def newcaptain_view(request, pk, cc):
    if request.method == 'POST':
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = AddCaptainForm(request.POST, team_name=equipa.nome)
        if form.is_valid():
            username = form.cleaned_data.get('jogadores')
            usuario_jogador = Profile.objects.get(first_name=username)
            capitao_novo = Jogador.objects.get(user_cc=usuario_jogador.cc, equipa=equipa)
            capitao_novo.capitao = True
            capitao_novo.save()

            print(capitao_novo, " Novo capitao")
            capitao_velho = Jogador.objects.get(user_cc=cc, equipa=equipa)
            capitao_velho.capitao = False
            capitao_velho.save()
            print(capitao_velho, "Ja nao e capitao")
            return redirect("bd-teamMenu", pk, cc)
    else:
        equipa = Equipa.objects.get(pk=pk)
        jogadores = Jogador.objects.filter(equipa=equipa)
        form = AddCaptainForm(team_name=equipa.nome)
    return render(request, 'newcaptain.html', {'form': form, 'jogadores': jogadores, 'pk': pk, 'cc': cc})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            if username == 'admin':
                Profile.objects.filter(pk=form.cleaned_data.get('cc')).update(admin=True)
                Profile.objects.filter(pk=form.cleaned_data.get('cc')).update(gestor_torneio=True)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('bd-home')

            else:
                user = Profile.objects.get(username=username)
                user.estado = False
                user.save()
                return render(request, 'notconfirmed.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile_view(request, pk=None):
    if pk:
        user = Profile.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)


def logout_view(request):
    logout(request)
    return redirect('bd-home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        teste = Profile.objects.get(username=username)
        if teste.estado:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('bd-home')
                else:
                    return HttpResponse("Your account is offline")

            else:
                return redirect('bd-login')
        if not teste.estado:
            return render(request, 'notconfirmed.html')
    else:
        return render(request, 'login.html', {})


def incTeams_view(request):
    equipas = Equipa.objects.filter(numTotalJogadores__lt=16)

    arg = {
        "equipasI": equipas
    }

    return render(request, 'equipasIncompletas.html', arg)


def teams_detail(request, pk):
    equipa = Equipa.objects.get(pk=pk)
    jogadores = Jogador.objects.filter(equipa=equipa)
    jogadoresTitularesGK = jogadores.filter(suplente=False, reserva=False, posicao="guarda-redes")
    jogadoresTitularesDefesas = jogadores.filter(suplente=False, reserva=False, posicao="defesa")
    jogadoresTitularesMedios = jogadores.filter(suplente=False, reserva=False, posicao="medio")
    jogadoresTitularesAvancados = jogadores.filter(suplente=False, reserva=False, posicao="avancado")
    jogadoresSuplentes = jogadores.filter(suplente=True)
    jogadoresReservas = jogadores.filter(reserva=True)

    args = {'pk': equipa.pk, 'equipa': equipa, "jogadoresTitularesGK": jogadoresTitularesGK,
            'jogadoresTitularesDefesas': jogadoresTitularesDefesas,
            "jogadoresTitularesMedios": jogadoresTitularesMedios,
            "jogadoresTitularesAvancados": jogadoresTitularesAvancados,
            "jogadoresSuplentes": jogadoresSuplentes, "jogadoresReservas": jogadoresReservas}

    return render(request, 'teamdetail.html', args)


def teams_detail2(request, pk, cc, ver0):
    equipa = Equipa.objects.get(pk=pk)
    jogadores = Jogador.objects.filter(equipa=equipa)
    jogadoresTitularesGK = jogadores.filter(suplente=False, reserva=False, posicao="guarda-redes")
    jogadoresTitularesDefesas = jogadores.filter(suplente=False, reserva=False, posicao="defesa")
    jogadoresTitularesMedios = jogadores.filter(suplente=False, reserva=False, posicao="medio")
    jogadoresTitularesAvancados = jogadores.filter(suplente=False, reserva=False, posicao="avancado")
    jogadoresSuplentes = jogadores.filter(suplente=True)
    jogadoresReservas = jogadores.filter(reserva=True)

    if ver0 == 1:
        ver = 1

    else:
        ver = 0
        users = Jogador.objects.filter(user_cc=cc)
        l = len(users)
        if l != 0:
            players = equipa.jogador_set.all()
            user = Jogador.objects.get(user_cc=cc)
            for p in players:
                if user == p:
                    ver = 1

    torneio = equipa.torneio

    args = {'pk': equipa.pk, "cc": cc, 'torneio': torneio, 'equipa': equipa, 'torneio': torneio, 'ver': ver,
            "jogadoresTitularesGK": jogadoresTitularesGK,
            'jogadoresTitularesDefesas': jogadoresTitularesDefesas,
            "jogadoresTitularesMedios": jogadoresTitularesMedios,
            "jogadoresTitularesAvancados": jogadoresTitularesAvancados,
            "jogadoresSuplentes": jogadoresSuplentes, "jogadoresReservas": jogadoresReservas}

    return render(request, 'teamdetail2.html', args)


def tournament_detail_view(request, pk, cc):
    torneio = Torneio.objects.get(pk=pk)
    equipas = Equipa.objects.filter(torneio=pk)
    equipas = equipas.order_by('pontos')
    numero = equipas.count()

    team_torn = Torneio.objects.get(pk=pk)
    players = Jogador.objects.filter(user_cc=cc)
    ver = 0
    for p in players:
        if p.equipa.torneio == team_torn:
            ver = 1

    gestor = torneio.gestor

    completas = 1
    for q in equipas:
        if q.numTotalJogadores < 16:
            completas = 0
            break

    args = {'torneio': torneio, 'equipas': equipas, 'numero': numero, 'ver': ver, 'gestor': gestor,
            'completas': completas}
    return render(request, 'tournamentinfo.html', args)


def tournament_guest_view(request, pk):
    torneio = Torneio.objects.get(pk=pk)
    equipas = Equipa.objects.filter(torneio=pk)
    equipas = equipas.order_by('pontos')
    numero = equipas.count()
    args = {'torneio': torneio, 'equipas': equipas, 'numero': numero}
    return render(request, 'tournamentinfoguest.html', args)


def createTournament_view(request):
    if request.method == "POST":
        form = CreateTournamentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bd-home')
    else:
        form = CreateTournamentForm()
    return render(request, 'addtournament.html', {'form': form})


def createTeam_view(request, pk):
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            pkequipa = form.cleaned_data.get('nome')
            args = {"pk": pkequipa}
            return redirect("bd-addcaptain", pkequipa)
    else:
        form = CreateTeamForm()
    return render(request, 'addteam.html', {'form': form, "pk": pk})


def createCaptain_view(request, pk):
    if request.method == "POST":
        form = CreatePlayerForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            equipas = Equipa.objects.all()
            equipa1 = equipas.get(pk=pk)
            jogadores = equipa1.jogador_set.all()
            pos = form.cleaned_data.get("posicao")
            jogador1 = jogadores.filter(posicao=pos)
            print(jogador1)
            jogador2 = jogador1.get(posicao=pos)
            jogador2.capitao = True
            jogador2.save()

            if form.cleaned_data.get("posicao") == "defesa":
                equipa = Equipa.objects.get(pk=pk)
                equipa.numDefesas = equipa.numDefesas + 1
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.save()
            if form.cleaned_data.get("posicao") == "medio":
                equipa = Equipa.objects.get(pk=pk)
                equipa.numMedios = equipa.numMedios + 1
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.save()
            if form.cleaned_data.get("posicao") == "avancado":
                equipa = Equipa.objects.get(pk=pk)
                equipa.numAvancados = equipa.numAvancados + 1
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.save()
            return redirect('bd-home')

    else:
        form = CreatePlayerForm()
    return render(request, 'addCaptain.html', {'form': form, "pk": pk})


def confirmation_view(request):
    listaUsers = Profile.objects.filter(estado=False)
    tamanho = len(listaUsers)
    if request.method == "POST":
        name_values = request.POST.getlist("Id")
        values = request.POST.getlist("tipo")
        i = 0
        while i < len(name_values):
            parametro_username = name_values[i]
            estado = values[i]
            profile = Profile.objects.get(username=parametro_username)
            if estado == "confirm":
                profile.estado = True
                profile.save()
                i = i + 1
            if estado == "not confirmed":
                profile.estado = False
                profile.save()
                i = i + 1
        args = {"listaUsers": listaUsers, "tamanho": tamanho}
        return render(request, 'confirmationMessage.html', args)

    args = {"listaUsers": listaUsers, "tamanho": tamanho}
    return render(request, 'confirmation.html', args)


def joinTeam_view(request, pk):
    if request.method == "POST":
        form = CreatePlayerForm(request.POST)
        if form.is_valid():

            try:

                form.save(commit=False)
                team = Equipa.objects.get(pk=pk)
                team_torn = team.torneio

                pk2 = form.cleaned_data.get("user_cc")
                players = Jogador.objects.filter(user_cc=pk2)

                for p in players:
                    if p.equipa.torneio == team_torn:
                        return render(request, 'errorteam.html')

            except Jogador.DoesNotExist:
                return render(request, 'error.html')

            form.save()
            if form.cleaned_data.get("posicao") == "defesa":
                equipa = Equipa.objects.get(pk=pk)
                if (equipa.numDefesas < equipa.DefesasTatica):
                    equipa.numDefesas = equipa.numDefesas + 1
                    equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                    equipa.save()
                    return redirect('bd-home')
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.numDefesasSuplentes = equipa.numDefesasSuplentes + 1
                equipa.save()
                return redirect('bd-home')

            if form.cleaned_data.get("posicao") == "medio":
                equipa = Equipa.objects.get(pk=pk)
                if (equipa.numMedios < equipa.MediosTatica):
                    equipa.numMedios = equipa.numMedios + 1
                    equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                    equipa.save()
                    return redirect('bd-home')
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.numMediosSuplentes = equipa.numMediosSuplentes + 1
                equipa.save()
                return redirect('bd-home')

            if form.cleaned_data.get("posicao") == "avancado":
                equipa = Equipa.objects.get(pk=pk)
                if (equipa.numAvancados < equipa.AvancadosTatica):
                    equipa.numAvancados = equipa.numAvancados + 1
                    equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                    equipa.save()
                    return redirect('bd-home')
                equipa.numTotalJogadores = equipa.numTotalJogadores + 1
                equipa.numAvancadosSuplentes = equipa.numAvancadosSuplentes + 1
                equipa.save()
                return redirect('bd-home')
    else:
        form = CreatePlayerForm()
    return render(request, 'jointeam.html', {'form': form, "pk": pk})


def manageteam_view(request, pk, cc):
    equipa = Equipa.objects.get(pk=pk)
    usuario = Jogador.objects.get(user_cc=cc, equipa=equipa)
    jogadores = Jogador.objects.filter(equipa=equipa)
    jogadoresGK = jogadores.filter(posicao="guarda-redes")
    jogadoresDefesas = jogadores.filter(posicao="defesa")
    jogadoresMedios = jogadores.filter(posicao="medio")
    jogadoresAvancados = jogadores.filter(posicao="avancado")

    if request.method == "POST":
        selected_values = request.POST.getlist("Id")
        values = request.POST.getlist("tipo")
        i = 0
        while i < len(selected_values):
            parametro_cc = selected_values[i]
            estado = values[i]
            jogador = Jogador.objects.get(user_cc=parametro_cc, equipa=equipa)
            jogador.titular = False
            jogador.suplente = False
            jogador.reserva = False
            if estado == "titular":
                jogador.titular = True
                jogador.save()
                i = i + 1
            if estado == "suplente":
                jogador.suplente = True
                jogador.save()
                i = i + 1
            if estado == "reserva":
                jogador.reserva = True
                jogador.save()
                i = i + 1

    args = {'pk': pk, 'cc': cc, 'usuario': usuario,
            'equipa': equipa,
            'jogadoresGK': jogadoresGK, 'jogadoresDefesas': jogadoresDefesas,
            'jogadoresMedios': jogadoresMedios,
            'jogadoresAvancados': jogadoresAvancados
            }
    return render(request, 'manageteam.html', args)


def make_games(request, pk):
    tournament = Torneio.objects.get(pk=pk)  # SELECT * FROM Torneio WHERE id = pk;
    equipas = Equipa.objects.filter(torneio=pk)  # SELECT * FROM Equipa WHERE Equipa.torneio = pk;
    estadios = Campo.objects  # SELECT * FROM Campo
    teams = []
    for equipa in equipas:
        teams.append(equipa.pk)

    firstTeam = teams[0]
    teams.pop(0)
    teste = Equipa.objects.get(pk=firstTeam)
    inicio = tournament.dataInicio
    dias1 = tournament.diasJogo
    horas = tournament.horarioInicio
    aux = datetime.datetime.today()
    aux = aux.replace(hour=horas.hour, minute=horas.minute)
    switcher = {"Segunda": 1, "Terça": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5, "Sábado": 6, "Domingo": 7}
    dias = switcher.get(dias1)

    aux1 = inicio.isoweekday()
    if (aux1 > dias):
        inicio += relativedelta(days=7 - (aux1 - dias))

    aux = aux.replace(day=inicio.day, month=inicio.month, year=inicio.year)
    halfSize = int(equipas.count() / 2)

    if (equipas.count() % 2) == 0:
        for i in range(0, equipas.count() - 1):
            print("ola")
            teamID = i % len(teams)
            teste2 = Equipa.objects.get(pk=teams[teamID])
            # INSERT INTO Jogo (equipaAGolos, equipaBGolos, equipa1, equipa2, torneio, campo, date) VALUES (0, 0, SELECT id FROM Equipa WHERE id=firstTeam, SELECT id FROM Equipa WHERE id=teams[twoTeam], SELECT id FROM Torneio WHERE id=pk, inicio)
            jogo = Jogo(equipaAGolos=0, equipaBGolos=0, equipa1=teste, equipa2=teste2, torneio=tournament,
                        campo=Campo.objects.get(pk=1), date=aux)
            jogo.save()
            for j in range(1, halfSize):
                print("teste", i, j)
                oneTeam = (i + j) % len(teams)
                twoTeam = (i + len(teams) - j) % len(teams)
                one = Equipa.objects.get(pk=teams[oneTeam])
                two = Equipa.objects.get(pk=teams[twoTeam])
                jogo = Jogo(equipaAGolos=0, equipaBGolos=0, equipa1=one, equipa2=two, torneio=tournament,
                            campo=Campo.objects.get(pk=j + 1), date=aux)
                jogo.save()
            aux += relativedelta(weeks=1)
        print(aux)
    else:
        for i in range(equipas.count() - 1):
            teamID = i % len(teams)
            jogo = Jogo(equipaAGolos=0, equipaBGolos=0, equipa1=teste, equipa2=teams[teamID], torneio=tournament,
                        campo=1, date=aux)
            jogo.save()
            for j in range(1, halfSize):
                oneTeam = (i + j) % len(teams)
                if (j == halfSize - 1):
                    twoTeam = (i + len(teams) - j) % len(teams)
                    one = Equipa.objects.get(pk=teams[oneTeam])
                    two = Equipa.objects.get(pk=teams[twoTeam])
                    jogo = Jogo(equipaAGolos=0, equipaBGolos=0, equipa1=one, equipa2=two, torneio=tournament,
                                campo=j + 1,
                                date=aux)
                    jogo.save()
            aux += relativedelta(weeks=1)

    jogos = Jogo.objects.filter(torneio=tournament)

    tournament.estado = 1
    tournament.save()

    args = {'jogos': jogos, 'torneio': tournament, 'pk': pk}

    return render(request, 'tourGames.html', args)


def estadoJogos(request, pk, cc):
    tournament = Torneio.objects.get(pk=pk)
    jogos = Jogo.objects.filter(torneio=tournament)

    jogadores = Jogador.objects.filter(user_cc=cc)
    player = None
    for j in jogadores:
        equipa = j.equipa
        if equipa.torneio == tournament:
            player = j

    now = datetime.datetime.now(timezone.utc) - relativedelta(minutes=120)

    ver1 = 0
    jg = None
    for jogo in jogos:
        jg = jogo

    if jg != None:
        data = jg.date
        if now >= data:
            tournament.estado = 2
            tournament.save()
            ver1 = 1

    args = {'jogos': jogos, 'torneio': tournament, 'now': now, 'jogador': player, 'ver1': ver1}
    return render(request, 'tourEstado.html', args)


def resultadosJogos(request, pk):
    tournament = Torneio.objects.get(pk=pk)
    jogos = Jogo.objects.filter(torneio=tournament)

    args = {'jogos': jogos, 'torneio': tournament}
    return render(request, 'infoRes.html', args)


def editarJogo(request, pk):
    jogo = Jogo.objects.get(pk=pk)
    if request.method == "POST":
        form = Resultado(request.POST)
        if form.is_valid():

            if (jogo.equipaAGolos != -1 and jogo.equipaBGolos != -1):

                anteriorA = jogo.equipaAGolos
                anteriorB = jogo.equipaBGolos

                if anteriorA > anteriorB:
                    jogo.equipa1.vitorias -= 1
                    jogo.equipa2.derrotas -= 1
                    jogo.equipa1.pontos -= 3

                elif anteriorA < anteriorB:
                    jogo.equipa1.derrotas -= 1
                    jogo.equipa2.vitorias -= 1
                    jogo.equipa2.pontos -= 3

                else:
                    jogo.equipa1.empates -= 1
                    jogo.equipa2.empates -= 1
                    jogo.equipa1.pontos -= 1
                    jogo.equipa2.pontos -= 1

            jogo.equipaAGolos = form.cleaned_data.get('resultado1')
            jogo.equipaBGolos = form.cleaned_data.get('resultado2')
            jogo.equipa1.golosMarcados += form.cleaned_data.get('resultado1')
            jogo.equipa1.golosSofridos += form.cleaned_data.get('resultado2')

            jogo.equipa2.golosMarcados += form.cleaned_data.get('resultado2')
            jogo.equipa2.golosSofridos += form.cleaned_data.get('resultado1')

            if jogo.equipaAGolos > jogo.equipaBGolos:
                jogo.equipa1.vitorias += 1
                jogo.equipa2.derrotas += 1
                jogo.equipa1.pontos += 3

            elif jogo.equipaAGolos < jogo.equipaBGolos:
                jogo.equipa1.derrotas += 1
                jogo.equipa2.vitorias += 1
                jogo.equipa2.pontos += 3

            else:
                jogo.equipa1.empates += 1
                jogo.equipa2.empates += 1
                jogo.equipa1.pontos += 1
                jogo.equipa2.pontos += 1

            jogo.save()




    else:
        form = Resultado()

    args = {'form': form, 'jogo': jogo}
    return render(request, 'editarJogo.html', args)


def Prox_Games_view(request):
    now = datetime.datetime.now()
    aux = now.isoweekday()
    ini = now + relativedelta(days=8 - aux)
    fim = ini + relativedelta(weeks=1)

    jogos = Jogo.objects.filter(date__gte=ini, date__lte=fim)
    equipas = Equipa.objects.all()

    # args = {'pk': pk, 'cc': cc, 'usuario': usuario,
    #       'equipa': equipa,
    #        'jogadoresGK': jogadoresGK, 'jogadoresDefesas': jogadoresDefesas,
    #        'jogadoresMedios': jogadoresMedios,
    #        'jogadoresAvancados': jogadoresAvancados
    #       }

    args = {'jogos': jogos, 'equipas': equipas}

    return render(request, 'proxSemana.html', args)


def melhoresMarcadores_view(request, pk):
    tournament = Torneio.objects.get(pk=pk)
    equipas = Equipa.objects.filter(torneio=tournament)
    i = 0
    aux = Jogador.objects.filter(golos=0)[:1].get()
    for equipa in equipas:
        jogadores = Jogador.objects.filter(equipa=equipa)
        for jogador in jogadores:
            if (i == 0):
                first = aux
                second = aux
                third = aux
                i += 1
            if (jogador.golos > first.golos):
                third = second
                second = first
                first = jogador
            elif (jogador.golos > second.golos):
                third = second
                second = jogador
            elif (jogador.golos > third.golos):
                third = jogador
            print(first.golos, second, third)

    args = {'first': first, 'second': second, 'third': third, 'pk': pk}
    return render(request, 'melhoresMarcadores.html', args)


def manageGestores_view(request):
    todosUsers = Profile.objects.all()
    if request.method == "POST":
        selected_usernames = request.POST.getlist("Id")
        values = request.POST.getlist("tipo")
        print(selected_usernames)
        print(values)
        i = 0
        while i < len(selected_usernames):
            parametro_user = selected_usernames[i]
            estado = values[i]
            userescolhido = Profile.objects.get(username=parametro_user)
            print(userescolhido.username)
            print(estado)
            if estado == "gestor":
                userescolhido.gestor_torneio = True
                userescolhido.save()
                i = i + 1
            if estado == "not gestor":
                userescolhido.gestor_torneio = False
                userescolhido.save()
                i = i + 1
        args = {'todosUsers': todosUsers}
        return render(request, 'managegestor.html', args)

    else:
        args = {'todosUsers': todosUsers}
        return render(request, 'managegestor.html', args)


def escrevenotifJogos(request, equipa, jogo):
    jogadores = Jogador.objects.filter(equipa=equipa)
    texto = "Jogo marcado para " + jogo.date + ", no campo: " + jogo.campo
    for jogador in jogadores:
        notif = Notificacao(notif=texto, pessoa=jogador)
        notif.save()


def notif_view(request, pk):
    user = Profile.objects.get(pk=pk)
    notifs = Notificacao.objects.filter(pessoa=user)
    args = {'notifs': notifs}
    return render(request, "notificacoes.html", args)


def escreveNotif_view(request, pk, cc):
    if request.method == "POST":
        form = NotificacaoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('bd-teamMenu', pk, cc )
    else:
        form = NotificacaoForm()
    return render(request, 'escrevenotificacao.html', {'form': form})


def expularJogadores_view(request, pk, cc):
    equipa = Equipa.objects.get(pk=pk)
    jogadores = Jogador.objects.filter(equipa=equipa)

    if request.method == "POST":
        selected_values = request.POST.getlist("Id")
        values = request.POST.getlist("tipo")
        i = 0
        while i < len(selected_values):
            parametro_cc = selected_values[i]
            estado = values[i]
            jogador = Jogador.objects.get(user_cc=parametro_cc, equipa=equipa)
            if estado == "kick":
                jogador.delete()
                i = i + 1
            if estado != "kick":
                i = i + 1

        args = {'pk': pk, 'cc': cc, 'jogadores': jogadores,
                'equipa': equipa,
                }
        return render(request, 'expulsarJogadores.html', args)
    else:

        args = {'pk': pk, 'cc': cc, 'jogadores': jogadores,
                'equipa': equipa,
                }
        return render(request, 'expulsarJogadores.html', args)
