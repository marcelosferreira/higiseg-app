from datetime import date
from multiprocessing.connection import Client
import re
from django.db import connections, OperationalError
from .models import ASO, Cliente
from ftplib import FTP, error_perm
from unidecode import unidecode


def userSiteValidation(user, password):
    valid = False
    conn = connections['mysql']
    with conn.cursor() as cursor:
        query = (f"SELECT * FROM `usuarios` WHERE `usuario` = '{user}' AND `senha` = '{password}'")
        cursor.execute(query)
        users = cursor.fetchall()
        if(users):
            valid = True
        else:
            valid = False
    return (valid)

def listarAsos(user):
    
    id = getUserId(user)
    conn = connections['mysql']
    with conn.cursor() as cursor:
        #FALTA: query = (f"SELECT id, texto, caminho, data FROM `documento` WHERE `idCliente` = '{id}'")
        query = (f"SELECT id, texto, caminho, data FROM `documento` WHERE `idCliente` = '13'")
        cursor.execute(query)
        results = cursor.fetchall()
        lista = []
        for row in results:
            id = row[0]
            funcionario = row[1]
            caminho = row[2]
            data = row[3]
            aso = ASO(id, funcionario, caminho, data, 'none')
            lista.append(aso)
    
    return(lista)

def getUserId(user):
    conn = connections['mysql']
    with conn.cursor() as cursor:
        query = (f"SELECT id FROM `usuarios` WHERE `usuario` = '{user}'")
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            id = result[0]

    return(id)

def detalheAso(user,id):
    conn = connections['mysql']
    idCliente = getUserId(user)
    with conn.cursor() as cursor:
        #FALTA query = (f"SELECT id, texto, caminho, data FROM `documento` WHERE `id` = '{id} AND `idCliente` = '{idCliente}'")
        query = (f"SELECT id, texto, caminho, data FROM `documento` WHERE `id` = '{id}'")
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            id = result[0]
            funcionario = result[1]
            caminho = result[2]
            data = result[3]
            aso = ASO(id, funcionario, caminho, data, 'none')
    return(aso)

def listarTodasEmpresas(user):
    conn = connections['mysql']
    idCliente = getUserId(user)
    with conn.cursor() as cursor:
        query = (f"SELECT id, nome FROM `usuarios`")
        cursor.execute(query)
        results = cursor.fetchall()
        lista = []
        for row in results:
            id = row[0]
            cliente = unidecode(row[1])
            empresa = Cliente(id, cliente)
            lista.append(empresa)
    
    return(lista)

def listarTodosAsos(user, id):
    conn = connections['mysql']
    idCliente = getUserId(user)
    with conn.cursor() as cursor:
        query = (f"SELECT doc.id, doc.texto, doc.caminho, doc.data, us.nome FROM `documento` as doc JOIN `usuarios` as us ON doc.idCliente = us.id  WHERE doc.idCliente = '{id}'")
        cursor.execute(query)
        results = cursor.fetchall()
        lista = []
        for row in results:
            id = row[0]
            funcionario = row[1]
            caminho = row[2]
            data = row[3]
            cliente = row[4]
            aso = ASO(id, funcionario, caminho, data, cliente)
            lista.append(aso)
    
    return(lista)

def detalheAsoAdmin(id):
    conn = connections['mysql']
    with conn.cursor() as cursor:
        query = (f"SELECT doc.id, doc.texto, doc.caminho, doc.data, us.nome FROM `documento` as doc JOIN `usuarios` as us ON doc.idCliente = us.id WHERE doc.id = '{id}'")
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            id = result[0]
            funcionario = result[1]
            caminho = result[2]
            data = result[3]
            cliente = result[4]
            aso = ASO(id, funcionario, caminho, data, cliente)

    return(aso)

def uploadAso(caminho_local, nome):
    hostname = 'ftp.higisegssma.com.br'
    login = 'higisegssma1'
    senha = 'higisegmA110569!'
    caminho_remoto = (f'/public_html/interno/docs/{nome}')
    try:
        ftp = FTP(hostname)
        ftp.login(login, senha)
        #ftp.cwd('/public_html/interno/docs/testee.txt')
        with open(caminho_local, "rb") as file:
            ftp.storbinary('STOR %s' % caminho_remoto, file)

        print("Upload concluído com sucesso!")
    except FileNotFoundError:
        print("Erro: Arquivo local não encontrado.")
    except error_perm as e:
        print(f"Erro de permissão: {str(e)}")
    except Exception as e:
        print(f"Erro desconhecido: {str(e)}")


def updateAso(id, caminho):
    conn = connections['mysql']
    data = date.today()
    caminho = (f"http://higisegssma.com.br/interno/docs/{caminho}")
    try:
        with conn.cursor() as cursor:
            query = (f"UPDATE `documento` SET `caminho` = %s, `data` = %s WHERE `id` = %s")
            values = (caminho, data, id)
            cursor.execute(query, values)
            conn.commit()
    except OperationalError as e:
        # Tratamento de erros específicos do banco de dados
        print(f"Erro ao executar a query: {str(e)}")
    except Exception as e:
        # Tratamento de erros gerais
        print(f"Erro desconhecido: {str(e)}")

def newAso(user, caminho, texto):
    conn = connections['mysql']
    data = date.today()
    caminho = (f"http://higisegssma.com.br/interno/docs/{caminho}")
    try:
        with conn.cursor() as cursor:
            query = (f"INSERT INTO `documento`(`caminho`, `texto`, `data`, `idCliente`) VALUES (%s, %s, %s, %s)")
            values = (caminho, texto, data, user)
            cursor.execute(query, values)
            conn.commit()
    except OperationalError as e:
        # Tratamento de erros específicos do banco de dados
        print(f"Erro ao executar a query: {str(e)}")
    except Exception as e:
        # Tratamento de erros gerais
        print(f"Erro desconhecido: {str(e)}")


def listarClientes():
    conn = connections['mysql']
    with conn.cursor() as cursor:
        query = "SELECT id, nome FROM `usuarios` WHERE `nivel` = 1 AND `ativo` = 1"
        cursor.execute(query)
        results = cursor.fetchall()
        lista = []
        for row in results:
            id = row[0]
            nome = row[1]
            cli = Cliente(id, nome)
            lista.append(cli)

    return(lista)

def deleteAso(id):
    conn = connections['mysql']
    try:
        with conn.cursor() as cursor:
            query = f"DELETE FROM `documento` WHERE `id` = '{id}'"
            cursor.execute(query)
        conn.commit()
        print("ASO deletado com sucesso!")
    except OperationalError as e:
        print(f"Erro de conexão com o banco de dados: {str(e)}")
    except Exception as e:
        print(f"Erro ao deletar o ASO: {str(e)}")

def tratarNomeFuncionario(nome):
    nome = nome.replace("ASO (", "")
    pattern = r"ASO\s*\d+\s*-\s*"
    nome = re.sub(pattern, "", nome)
    nome.split()
    nome = nome.replace("ASO - (", "")
    nome = nome.replace("ASO - ", "")
    nome = nome.replace("ASOV - ", "")
    nome = nome.replace("ASO ", "")
    nome = nome.replace("ATESTADO ", "")
    if len(nome) > 20:
            nome = nome[:20] + '...'

    return nome

def tratarCaminho(path):
    path = path.replace("http://", "https://")
    
    return path