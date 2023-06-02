from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.base, name='base'),

    path('novo/', views.newUser, name='new_user'), #d
    path('users/', views.users, name='users'), #d
    path('users/delete/<int:userId>', views.deleteUser, name='delete_user'), #d
    
    path('login/', views.login, name='login'), #D

    path('listaAsos/', views.listaAsos, name='lista_asos'), #d
    path('detalheAso/<int:asoId>', views.detalheAso, name='detalhe_aso'), #d
    path('downloadAso/<int:asoId>', views.downloadAso, name='download_aso'), #d
    path('listaEmpresasAdmin/', views.listaEmpresasAdmin, name='lista_empresas_admin'), #d
    path('listaAsosAdmin/<int:asoId>', views.listaAsosAdmin, name='lista_asos_admin'), #d
    path('alterarAso/<int:asoId>', views.alterarAso, name='alterar_aso'), #d
    path('deleteAso/<int:asoId>', views.deleteAso, name='delete_aso'), #d
    path('novoAso/', views.novoAso, name='novo_aso'), #d

    path('listaAgendamentos/', views.listaAgendamentos, name='lista_agendamentos'), #d
    path('novoAgendamento/', views.novoAgendamento, name='novo_agendamento'), #d
    path('listaAgendamentosAdmin/', views.listaAgendamentosAdmin, name='lista_agendamentos_admin'), #d
    path('alterarAgendamento/<int:agendamentoId>', views.alterarAgendamento, name='alterar_agendamento'), #d
    path('deleteAgendamento/<int:agendamentoId>', views.deleteAgendamento, name='delete_agendamento'), #d

]
