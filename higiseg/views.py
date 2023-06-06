from datetime import date
from email import message
import os
import tempfile
import requests
import logging
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm
from apphigiseg.settings import BASE_DIR, STATIC_URL, STATICFILES_DIRS
from .models import Agendamento, Funcionario, User, ASO, Agendamento, Cliente_idClienteWeb
from .forms import AgendamentoForm
from . import utils
from django.db import connections
from django.core.mail import send_mail

logger = logging.getLogger('APPHIGISEG')
##
#### INICIO
##
def ini(request):
    return render(request, 'ini.html')

def base(request):
    return render(request, 'home.html')

def quemSomos(request):
    return render(request, 'quemSomos.html')

def servicos(request):
    return render(request, 'servicos.html')

def offline(request):
    return render(request, 'offline.html')

def contato(request):
    if request.method == 'POST':
        try:
            nome = request.POST['nome']
            email = request.POST['email']
            mensagem = request.POST['mensagem']
            send_mail(
                "Contato do Site:",
                f"Nome: {nome}\nEmail: {email}\n\n{mensagem}",
                email,
                ['destinatario@example.com'],
                fail_silently=False,
            )
            messages.success(request, 'Mensagem enviada com sucesso.')
        except Exception as e:
            logger.error(f"users: Ocorreu um erro: {str(e)}")
            messages.error(request, 'Mensagem não enviada, entre em contato com o suporte.')
    
    return render(request, 'contato.html')

##
#### CONTROLE DE USUÁRIOS
##
def login(request): #d
    if request.user.is_authenticated:
        return redirect('base')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('lista_empresas_admin')
                else:
                    return redirect('lista_asos')
            else:
                logger.error('Ocorreu um erro: Senha e/ou user inválido')
                messages.error(request, 'Usuário ou senha inválidos.') #FALTA template modais msg

    return render(request, 'login.html')

def newUser(request): #d
    if request.method=='POST':
        user = request.POST['username']
        sitePassword = request.POST['sitePassword']
        password = request.POST['password']
        try:
            usuario = User.objects.get(username = user)
            messages.error(request, 'Usuário já cadastrado no sistema.') #FALTA template modais msg
        except:
            if(utils.userSiteValidation(user, sitePassword)):
                try:
                    id = utils.getUserId(user)
                    u = User.objects.create_user(user, None, password)
                    c = Cliente_idClienteWeb.objects.create(userCliente = u, nomeCliente = user, idClienteWeb = id)
                    messages.success(request, 'Usuário criado com sucesso.') #FALTA template modais msg
                except:
                    logger.error(f'Falha na tentativa de novo cadastro no sistema - User: {user}')
                    messages.error(request, 'Cadastrado não realizado. Entre em contato com o suporte!') #FALTA template modais msg
            else:
                logger.error(f'Falha na tentativa de novo cadastro no sistema - User Id: {user}')
                messages.error(request, 'Usuário e/ou senha do portal incorretos. Entre em contato com o suporte!') #FALTA template modais msg

    return render(request, 'newUser.html')

def esqueciSenha(request):
    #FALTA: tudo
    return (request)

@login_required
@staff_member_required
def users(request):
    try:
        users = User.objects.filter(is_staff=False)
    except Exception as e:
        logger.error(f"users: Ocorreu um erro: {str(e)}")

    return render(request, 'users.html', {'users': users})

@login_required #d
@staff_member_required
def deleteUser(request, userId):
    try:
        user = User.objects.get(pk=userId)
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('users')
    except ObjectDoesNotExist:
        logger.error(f"Usuário não existe: {user}")
        messages.error(request, 'Usuário não identificado. Entre em contato com o suporte!')
        return redirect('users')
    except ProtectedError:
        logger.error(f"Usuário protegido: {user}")
        messages.error(request, 'Usuário protegido. Entre em contato com o suporte!')
        return redirect('users')

##
#### CONTROLE DE ASOS
##
@login_required #d
def listaAsos(request):
    try:
        user = get_object_or_404(User, pk=request.user.pk)
        asos = utils.listarAsos(user.username)
        for aso in asos:
            aso.funcionario = utils.tratarNomeFuncionario(aso.funcionario)
    except Exception as e:
        logger.error(f"listaAsos: Ocorreu um erro: {str(e)}")
        
    return render(request, 'listaAsos.html', {'asos': asos})

@login_required #d
def detalheAso(request,asoId):
    try:
        user = User.objects.get(pk=request.user.pk)
        aso = utils.detalheAso(user.username, asoId)
    except Exception as e:
        logger.error(f"detalheAso: Ocorreu um erro: {str(e)}")
                
    return render(request, 'detalheAso.html', {'aso': aso})

@login_required #d
def downloadAso(request, asoId):
    try:
        user = User.objects.get(pk=request.user.pk)
        aso = utils.detalheAso(user.username, asoId)
        file_url = aso.caminho
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ASO.pdf"'
        pdf_data = requests.get(file_url).content
        response.write(pdf_data)
    except Exception as e:
        logger.error(f"downloadAso: Ocorreu um erro: {str(e)}")
    
    return response

@login_required
@staff_member_required #d
def listaEmpresasAdmin(request):
    try:
        user = User.objects.get(pk=request.user.pk)
        empresas = utils.listarTodasEmpresas(user.username)
    except Exception as e:
        logger.error(f"listaEmpresasAdmin: Ocorreu um erro: {str(e)}")
    
    return render(request, 'listaEmpresasAdmin.html', {'empresas': empresas})

@login_required
@staff_member_required
def listaAsosAdmin(request,asoId): #d
    try:
        user = User.objects.get(pk=request.user.pk)
        asos = utils.listarTodosAsos(user.username,asoId)
        empresa = "None"
        for aso in asos:
            aso.funcionario = utils.tratarNomeFuncionario(aso.funcionario)
            empresa = aso.cliente
    except Exception as e:
        logger.error(f"listaEmpresasAdmin: Ocorreu um erro: {str(e)}")
    
    return render(request, 'listaAsosAdmin.html', {'asos': asos, 'empresa':empresa})

@login_required
@staff_member_required
def alterarAso(request, asoId): #d
    user = User.objects.get(pk=request.user.pk)
    aso = utils.detalheAsoAdmin(asoId)
    if request.method == 'POST':
        try:
            arquivo = request.FILES['file']
            nome = (f"{aso.funcionario}-{date.today()}.pdf")
            destino = os.path.join(settings.MEDIA_ROOT, nome)
            print(destino)
            with open(destino, 'wb') as file:
                for chunk in arquivo.chunks():
                    file.write(chunk)
            utils.uploadAso(destino, nome)
            utils.updateAso(asoId, nome)
            messages.success(request, 'ASO alterado com sucesso.')     
        except KeyError:
            logger.error(f"alterarAso: Ocorreu um erro: {user}")
            messages.error(request, 'Nenhum arquivo foi inserido.')
    
    return render(request, 'alterarAso.html', {'aso': aso})

@login_required
@staff_member_required
def novoAso(request):   #d
    user = User.objects.get(pk=request.user.pk)
    clientes = utils.listarClientes()
    if request.method == 'POST':
        try:
            arquivo = request.FILES['file']
            funcionario = request.POST['texto']
            clienteId = request.POST['cliente']
            nome = (f"{funcionario}-{date.today()}.pdf")
            destino = os.path.join(settings.MEDIA_ROOT, nome)
            with open(destino, 'wb') as file:
                for chunk in arquivo.chunks():
                    file.write(chunk)
            utils.uploadAso(destino, nome)
            utils.newAso(clienteId, nome, funcionario)
            messages.success(request, 'ASO inserido com sucesso.')        
        except KeyError:
            logger.error(f"novoAso: Ocorreu um erro: {user}")
            messages.error(request, 'Nenhum arquivo foi inserido.')
        
    return render(request, 'newAso.html', {'clientes':clientes})

@login_required
@staff_member_required
def deleteAso(request, asoId): #d
    try:
        user = User.objects.get(pk=request.user.pk)
        utils.deleteAso(asoId)
        messages.success(request, 'ASO excluído com sucesso.')
    except Exception as e:
        logger.error(f"deleteAso: Ocorreu um erro: {str(e)}")
    
    return redirect('lista_empresas_admin')

##
#### CONTROLE DE AGENDAMENTOS
##
@login_required
def listaAgendamentos(request): #d
    try:
        user = User.objects.get(pk=request.user.pk)
        agendamentos = Agendamento.objects.filter(funcionarioAgendamento__userClienteFuncionario=user)
    except Exception as e:
        logger.error(f"listaAgendamentos: Ocorreu um erro: {str(e)}")
    return render(request, 'agendamentos.html', {'agendamentos': agendamentos})

@login_required
@staff_member_required
def novoAgendamento(request): #d
    try:
        if request.method == "POST":
            form = AgendamentoForm(request.POST)
            if form.is_valid():
                agendamento = form.save(commit=False)
                agendamento.userAdminAgendamento = request.user
                agendamento.save()
                messages.success(request, 'Agendamento salvo com sucesso.') 
            else:
                messages.error(request, 'Ocorreu algum erro, verifique novamente.')
        else:
            form = AgendamentoForm()
    except Exception as e:
        logger.error(f"novoAgendamento: Ocorreu um erro: {str(e)}")
    
    return render(request, 'newAgendamento.html', {'form': form})

@login_required
@staff_member_required
def listaAgendamentosAdmin(request): #d
    try:
        user = User.objects.get(pk=request.user.pk)
        agendamentos = Agendamento.objects.all
    except Exception as e:
        logger.error(f"listaAgendamentosAdmin: Ocorreu um erro: {str(e)}")
    
    return render(request, 'agendamentos.html', {'agendamentos': agendamentos, 'user': user})

@login_required
@staff_member_required
def alterarAgendamento(request, agendamentoId): #d
    try:
        agendamento = get_object_or_404(Agendamento, id=agendamentoId)
        if request.method == 'POST':
            form = AgendamentoForm(request.POST, instance=agendamento)
            if form.is_valid():
                form.save()
                messages.success(request, 'Agendamento alterado com sucesso.') 
            else:
                messages.error(request, 'Ocorreu algum erro, verifique novamente.') 
        else:
            form = AgendamentoForm(instance=agendamento)
    except Exception as e:
        logger.error(f"alterarAgendamento: Ocorreu um erro: {str(e)}")
    
    return render(request, 'alterarAgendamento.html', {'form': form, 'agendamento': agendamento})

@login_required
@staff_member_required
def deleteAgendamento(request, agendamentoId): #d
    try:
        agendamento = get_object_or_404(Agendamento, pk=agendamentoId)
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso.')
    except Exception as e:
        logger.error(f"deleteAgendamento: Ocorreu um erro: {str(e)}")
    
    return redirect('lista_agendamentos_admin')