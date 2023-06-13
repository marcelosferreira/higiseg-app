from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.ini, name='ini'),
    path('home/', views.base, name='base'),
    path('quemSomos/', views.quemSomos, name='quem_somos'),
    path('servicos/', views.servicos, name='servicos'),
    path('contato/', views.contato, name='contato'),
    path('offline/', views.offline, name='offline'),

    path('novo/', views.newUser, name='new_user'),
    path('users/', views.users, name='users'),
    path('users/delete/<int:userId>', views.deleteUser, name='delete_user'),
    
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('listaAsos/', views.listaAsos, name='lista_asos'),
    path('detalheAso/<int:asoId>', views.detalheAso, name='detalhe_aso'),
    path('downloadAso/<int:asoId>', views.downloadAso, name='download_aso'),
    path('listaEmpresasAdmin/', views.listaEmpresasAdmin, name='lista_empresas_admin'),
    path('listaAsosAdmin/<int:asoId>', views.listaAsosAdmin, name='lista_asos_admin'),
    path('alterarAso/<int:asoId>', views.alterarAso, name='alterar_aso'),
    path('deleteAso/<int:asoId>', views.deleteAso, name='delete_aso'),
    path('novoAso/', views.novoAso, name='novo_aso'),

    path('listaAgendamentos/', views.listaAgendamentos, name='lista_agendamentos'),
    path('novoAgendamento/', views.novoAgendamento, name='novo_agendamento'),
    path('listaAgendamentosAdmin/', views.listaAgendamentosAdmin, name='lista_agendamentos_admin'),
    path('alterarAgendamento/<int:agendamentoId>', views.alterarAgendamento, name='alterar_agendamento'),
    path('deleteAgendamento/<int:agendamentoId>', views.deleteAgendamento, name='delete_agendamento'),

]
