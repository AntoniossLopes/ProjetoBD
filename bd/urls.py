from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='bd-home'),
    path('signup/', views.signup_view, name='bd-signup'),
    path('login/', views.login_view, name='bd-login'),
    path('logout/', views.logout_view, name='bd-logout'),
    path('profile/', views.profile_view, name='bd-profile'),
    path('addtournament/', views.createTournament_view, name='bd-addtour'),
    path('changeProfile/<int:pk>', views.changeProfile_view, name='bd-changeProfile'),
    path('tournamentinfo/<int:pk>', views.tournament_guest_view, name='bd-tournamentGuest'),
    path('tournamentinfo/<int:pk>/<int:cc>', views.tournament_detail_view, name='bd-infotour'),
    path('myteam/<int:pk>', views.myTeam_view, name="bd-myteam"),
    path('teammenu/<str:pk>/<int:cc>', views.teamMenu_view, name="bd-teamMenu"),
    path('playerinfo/<str:pk>/<int:cc>/<int:ccplayer>', views.jogador_view, name="bd-playerinfo"),
    path('playerinfo/<str:pk>/<int:cc>/<int:ccplayer>/<int:ver0>', views.jogadortour_view, name="bd-playerinfotour"),
    path('playerinfo/<str:pk>/<int:ccplayer>', views.jogadorguest_view, name="bd-playerinfoguest"),
    path('newcaptain_view/<str:pk>/<int:cc>',views.newcaptain_view, name="bd-newcaptain"),
    path('equipasIncompletas/',views.incTeams_view, name="bd-equipasInc"),
    path('faltasatrasos/<str:pk>/<int:cc>', views.faltasPagamentos_view, name="bd-faltasPagamentos"),
    path('manageteam/<str:pk>/<int:cc>', views.manageteam_view, name="bd-manageteam"),
    path('teaminfo/<str:pk>', views.teams_detail, name='bd-teamdetail'),
    path('teaminfo/<str:pk>/<int:cc>/<int:ver0>', views.teams_detail2, name='bd-teamdetail2'),
    #path('addcaptain/<slug:pk>', views.createCaptain_view, name='bd-addcaptain'),
    path('addcaptain/<str:pk>', views.createCaptain_view, name='bd-addcaptain'),
    path('createTeam/<int:pk>', views.createTeam_view, name='bd-createTeam'),
    path('joinTeam/<str:pk>', views.joinTeam_view, name='bd-joinTeam'),
    path('permissoes/', views.users_view, name='bd-permissoes'),
    path('permissoes/<int:pk>', views.permissoes_view, name='bd-permissoes'),
    path('proxSemana/', views.Prox_Games_view, name='bd-proxSemana'),
    path('estadoJogos/<int:pk>/<int:cc>', views.estadoJogos, name='bd-estadoJogos'),
    path('resJogos/<int:pk>', views.resultadosJogos, name='bd-infoRes'),
    path('editGame/<int:pk>', views.editarJogo, name='bd-editarJogo'),
    path('geraJogos/<int:pk>', views.make_games, name='bd-geraJogos'),
    path('proxjogos/', views.Prox_Games_view, name='bd-jogos'),
    path('confirmation/', views.confirmation_view, name='bd-confirmation'),
    path('registarfaltas/<str:pk>/<int:cc>', views.faltasAtraso_view, name='bd-registaFaltas'),
    path('managegestores/', views.manageGestores_view, name='bd-managegestores'),
    path('expulsar/<str:pk>/<int:cc>', views.expularJogadores_view, name="bd-expusarjogadores"),
    path('escrevenotificacao/<str:pk>/<int:cc>', views.escreveNotif_view, name='bd-escrevenotif'),
    path('notificacoes/<str:pk>', views.notif_view, name='bd-notificacoes'),
    path('melhoresMarcadores/<int:pk>', views.melhoresMarcadores_view, name='bd-melhoresMarcadores'),
]
