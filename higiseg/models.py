from http import client
from io import RawIOBase
from signal import SIG_DFL
from django.db import models
from django.contrib.auth.models import User

class ASO:
    def __init__(self, id, funcionario, caminho, data, cliente):
        self.id = id
        self.funcionario = funcionario
        self.caminho = caminho
        self.data = data
        self.cliente = cliente

class Cliente:
    def __init__(self, id, cliente):
        self.id = id
        self.cliente = cliente

class Funcionario(models.Model):
    nomeFuncionario = models.CharField(max_length=255)
    descricaoFuncionario = models.CharField(max_length=255, blank=True, null=True)
    idadeFuncionario = models.CharField(max_length=4, blank=True, null=True)
    sexoFuncionario = models.CharField(max_length=2, blank=True, null=True)
    userClienteFuncionario = models.ForeignKey(User, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.nomeFuncionario

class Agendamento(models.Model):
    funcionarioAgendamento = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    dataAgendamento = models.DateTimeField()
    userAdminAgendamento = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.funcionarioAgendamento.nomeFuncionario

class Cliente_idClienteWeb(models.Model):
    userCliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nomeCliente = models.CharField(max_length=255)
    idClienteWeb = models.CharField(max_length=4)

    def __str__(self):
        return self.nomeCliente