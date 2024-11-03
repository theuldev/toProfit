import os
import psutil
import random
import zipfile
import requests
from flask import Flask
import threading
import pandas as pd
from time import sleep
from faker import Faker
from pathlib import Path
import customtkinter as ctk
from customtkinter import *
from unidecode import unidecode
from selenium import webdriver
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urlunparse, ParseResult
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
from tkinter import *
import string
from selenium_stealth import stealth
from PIL import Image
import wget
import subprocess
import shutil
import platform
app = Flask(__name__)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
import asyncio

UPDATE_URL = "https://github.com/theuldev/toProfit/blob/main/Toprofit-v3.1.exe?raw=true"
LOCAL_EXECUTABLE = "Toprofit-v3.1.exe"  # Nome do executável atual
TEMP_DOWNLOAD_PATH = "temp/Toprofit-v3.1.exe"  # Caminho temporário para download
UPDATE_LOCK = "update_completed.lock"  # Arquivo de marcação para verificar se atualização já ocorreu


url_add_user = ""
url_consultar_mac_user = ""
url_consultar_chave = ""

url_main = "http://http://146.190.41.205:5000/toprofit"
def start_in_multithread(function, *args, **kwargs):
    def wrapper():
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(f"Erro na thread: {e}")

    thread = threading.Thread(target=wrapper)
    thread.start()
def message_success(mensagem):
    # Mostrar alguma mensagem positiva com ícone de sucesso.
    CTkMessagebox(message=mensagem, icon="check", option_1="Ok")


def message_erro(mensagem):
    # Mostrar mensagens de erros.
    CTkMessagebox(title="Erro", message=mensagem, icon="cancel")

# Obter o endereço MAC ADDRESS


def obter_endereco_mac():
    try:
        interfaces = psutil.net_if_addrs()
        for interface, endereco in interfaces.items():
            for info in endereco:
                if info.family == psutil.AF_LINK:
                    return info.address
    except:
        return None


def dados_licenca(licenca):
    url_get = f"http://146.190.41.205:5000/toprofit/validarchave/{licenca}"
    response = requests.get(url=url_get)
    data = response.json()
    acesso = data['acesso']

    if acesso == True:
        try:
            data_limite = data['validade']
        except:
            data_limite = None
        try:
            status = data['status']
        except:
            status = None

    return acesso, data_limite, status

# Verificar se o MAC está associado a alguma licença, se não estiver mandar pra tela de escolher uma licença


def consultar_permissao_computador():
    mac_address = obter_endereco_mac()
    url_get = f"{url_main}/verificar_acesso/{mac_address}"
    #url_get = f"http://146.190.41.205:5000/toprofit/verificar_acesso/{mac_address}"
    try:
        response = requests.get(url=url_get)
        data = response.json()
        acesso = data['acesso']
        mensagem = data['mensagem']
        return acesso, mensagem
    except:
        try:
            mensagem = data['mensagem']
            acesso = False
            return acesso, mensagem
        except:
            return False, "Error"

def login_app():
    

    login = CTk()
    login.geometry("600x480")
    login.resizable(0,0)
    
    side_img_data = Image.open(".\\shared\\images\\login-screen.png")
    email_icon_data = Image.open(".\\shared\\images\\email_icon.png")
    password_icon_data = Image.open(".\\shared\\images\\password_icon.png")

    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

    CTkLabel(master=login, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=login, width=300, height=480)
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")
        
    CTkLabel(master=frame, text="Bem-vindo de volta!", text_color="#fff", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Acesse a sua conta.", text_color="#fff", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Email:", text_color="#fff", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    email_entry = CTkEntry(master=frame, width=225, fg_color="#2A2A2A", border_color="#1C72B0", border_width=1, text_color="#1C72B0")
    email_entry.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Senha:", text_color="#fff", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    password_entry = CTkEntry(master=frame, width=225, fg_color="#2A2A2A", border_color="#1C72B0", border_width=1, text_color="#1C72B0", show="*")
    password_entry.pack(anchor="w", padx=(25, 0))
    
    CTkLabel(master=frame, text="  Licença:", text_color="#fff", anchor="w", justify="left", font=("Arial Bold", 14), compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    license_entry = CTkEntry(master=frame, width=225, fg_color="#2A2A2A", border_color="#1C72B0", border_width=1, text_color="#1C72B0")
    license_entry.pack(anchor="w", padx=(25, 0))
    
    error_label = CTkLabel(master=frame, text="", text_color="red", font=("Arial", 12))
    error_label.pack(anchor="w", padx=(25, 0), pady=(10, 0))

    btn_login = CTkButton(master=frame, text="Login", fg_color="#1C72B0", hover_color="#0E4C78", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=lambda:start_in_multithread(func_login)).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    
    def func_login():
        e_email = email_entry.get()
        e_password = password_entry.get()
        e_license = license_entry.get()
        e_license = e_license.replace("\n", "").replace("\r", "")
        def delete_field(field):
            try: 
                field.delete(0, ctk.END)
            except Exception as e:
                print(e)
                pass
            
        
        if len(e_email) == 0:
            delete_field(license_entry)
            message_erro("Você não inseriu nenhum email!")
        
        
        if len(e_password) == 0:
            delete_field(license_entry)
            message_erro("Você não inseriu nenhuma senha!")
            return
        if " " in e_password:
            delete_field(password_entry)
            message_erro("Sua senha não pode ter espaços!")
            return
        if len(e_license) < 24:
            delete_field(license_entry)
            message_erro("Você inseriu uma licença curta!")
            return
        if len(e_license) > 35:
            delete_field(license_entry)
            message_erro("Você inseriu uma licença longa!")
            return
        if len(e_password) < 5:
            delete_field(password_entry)
            message_erro("Você inseriu uma senha muito curta!")
            return
        
            
            
        try:
            response = requests.post(f"{url_main}/login", json={"email": e_email, "senha": e_password, "license": e_license})

            if response.status_code == 201:
                jwt_token = response.json().get('token')
                if jwt_token:
                    app.config['JWT_TOKEN'] = jwt_token
                
                    try:
                        url_consultar_chave = f"{url_main}/validarchave/{e_license}"
                        response_chave = requests.get(url=url_consultar_chave).json()
                        acesso = response_chave['acesso']
                        if acesso == True:
                            validade = response_chave['validade']
                            url_consultar_chave = f"{url_main}/update_license/{e_email}/{e_license}"
                            dados_licenca_user = {
                                'email': f'{e_email}',
                                'licenca': f'{e_license}'
                            }

                            response = requests.put(
                                url=url_consultar_chave, json=dados_licenca_user)
                            response = response.json()
                            mensagem = response['mensagem']
                            if mensagem == "Data limite do usuário atualizada com sucesso":
                                app.config['email'] = e_email
                                
                                
                                message_success(
                                    f"Licença ativada com sucesso, essa é uma licença {validade}")
                                sleep(3)
                                login.withdraw()
                                start_in_multithread(auth_2fa)    
                            
                            elif mensagem == "Licença inválida ou já usada":
                                return message_erro("Licença inválida ou já usada")
                        else:
                            return message_erro("Você inseriu uma licença inválida")

                    except Exception as e:
                        return  message_erro("Você inseriu uma licença inválida")
                else:
                    message_erro("Você inseriu uma licença inválida")
                    
                    

            else:
                error_label.configure(text="Falha no login: Verifique suas credenciais.")
        
        except Exception as e:
            error_label.configure(text=f"Erro ao conectar: {str(e)}")


    login.mainloop()
def auth_2fa():
   
    two_fa_window = CTk()
    two_fa_window.geometry("400x300")
    two_fa_window.title("Autenticação de Dois Fatores")

    CTkLabel(two_fa_window, text="Insira o código de 2FA", font=("Arial Bold", 16)).pack(pady=20)

    CTkLabel(two_fa_window, text="Código 2FA:", font=("Arial", 12)).pack(pady=10)
    token_entry = CTkEntry(two_fa_window, width=200)
    token_entry.pack(pady=10)
    
        
    def verify_2fa():
 
        token_2fa = token_entry.get()
        mac_address = obter_endereco_mac()
        json = {"token":token_2fa, "mac_address": mac_address }
        response = requests.post(f"{url_main}/token/verify_2fa", json=json, headers= {'x-access-token': app.config['JWT_TOKEN']})

        if response.status_code == 200:
            print("Autenticação de 2FA bem-sucedida!")
            two_fa_window.withdraw()  
            app_principal()
        else:
            return message_erro("Código inválido, tente novamente")
    def retry_token(): 
        json = {"email":app.config['email']}
        response = requests.post(f"{url_main}/token/retry_token", json=json, headers= {'x-access-token': app.config['JWT_TOKEN']})
        if response.status_code == 200:
            message_success("Foi enviado um código no email")
        else:
            message_erro("Houve um erro ao enviar o código")
            
    

    CTkButton(two_fa_window,text="Verificar", command=lambda:start_in_multithread(verify_2fa)).pack(pady=20)
    CTkButton(two_fa_window,text="Reenviar token", command= lambda:start_in_multithread(retry_token)).pack(pady=20)
    two_fa_window.mainloop()
    
    
def janela_licenca_app():
    janela_licenca = ctk.CTk()
    janela_licenca.geometry("500x420")

    janela_licenca.maxsize(width=500, height=350)
    janela_licenca.resizable(False, False)
    janela_licenca.title("Autenticação do Sistema")

    # Cadastrar endereço MAC do usuário
    def apagar_campos():
        campo_licenca_app.delete(0, ctk.END)
        campo_nome_app.delete(0, ctk.END)
        campo_senha_app.delete(0, ctk.END)

    # Texto inicial do programa
    texto = ctk.CTkLabel(janela_licenca, text="Autenticação - ToProfit",
                         anchor="center", font=("arial bold", 26))
    texto.pack(padx=20, pady=25)

    # Campo e etiqueta para digitar o nome pro App
    ctk.CTkLabel(janela_licenca, text="Usuario:",
                 font=("arial bold", 14)).place(x=100, y=65)
    campo_nome_app = ctk.CTkEntry(
        janela_licenca, placeholder_text="Insira seu usuário...", width=250, height=30)
    campo_nome_app.pack(padx=10, pady=15)

    ctk.CTkLabel(janela_licenca, text="Senha:", font=(
        "arial bold", 14)).place(x=100, y=135)
    campo_senha_app = ctk.CTkEntry(
        janela_licenca, placeholder_text="Insira a sua senha...", show="*", width=250, height=30)
    campo_senha_app.pack(padx=10, pady=25)

    ctk.CTkLabel(janela_licenca, text="Licença/chave:",
                 font=("arial bold", 14)).place(x=100, y=210)
    campo_licenca_app = ctk.CTkEntry(
        janela_licenca, placeholder_text="Insira a sua licença...", width=250, height=30)
    campo_licenca_app.pack(padx=10, pady=20)

    def verify_licenca():
        licenca_inserida = campo_licenca_app.get()
        nome_inserido = campo_nome_app.get()
        senha_inserida = campo_nome_app.get()
        mac_address = obter_endereco_mac()

        if len(nome_inserido) < 4:
            apagar_campos()
            message_erro("Você inseriu um nome muito curto!")
            return bttn_ativar_licenca.configure(state="normal")
        if len(licenca_inserida) < 24:
            apagar_campos()
            message_erro("Você inseriu uma licença curta!")
            return bttn_ativar_licenca.configure(state="normal")

        if len(nome_inserido) > 15:
            apagar_campos()
            message_erro("Você inseriu um nome muito grande!")
            return bttn_ativar_licenca.configure(state="normal")
        if len(licenca_inserida) > 35:
            apagar_campos()
            message_erro("Você inseriu uma licença inválida!")
            return bttn_ativar_licenca.configure(state="normal")

        if len(senha_inserida) < 5:
            apagar_campos()
            message_erro("Você inseriu uma senha muito curta!")
            return bttn_ativar_licenca.configure(state="normal")
        if " " in senha_inserida:
            apagar_campos()
            message_erro("Sua senha não pode ter espaços!")
            return bttn_ativar_licenca.configure(state="normal")

        url_add_user = "http://146.190.41.205:5000/toprofit/verifyuser"

        dados = {
            "nome": f"{nome_inserido}",
            "senha": f"{senha_inserida}",
            "mac_address": f"{mac_address}"
        }

        response_create = requests.post(url=url_add_user, json=dados)
        data = response_create.json()
        mensagem = data['mensagem']

        if response_create.status_code == 201:
            try:
                url_consultar_chave = f"http://146.190.41.205:5000/toprofit/validarchave/{licenca_inserida}"
                response_chave = requests.get(url=url_consultar_chave).json()
                acesso = response_chave['acesso']
                if acesso == True:
                    validade = response_chave['validade']
                    url_consultar_chave = f"http://146.190.41.205:5000/toprofit/update_license/{nome_inserido}/{licenca_inserida}"
                    dados_licenca_user = {
                        'nome': f'{nome_inserido}',
                        'licenca': f'{licenca_inserida}'
                    }

                    response = requests.put(
                        url=url_consultar_chave, json=dados_licenca_user)
                    response = response.json()
                    mensagem = response['mensagem']
                    if mensagem == "Data limite do usuário atualizada com sucesso":
                        message_success(
                            f"Licença ativada com sucesso, essa é uma licença {validade}")
                        app_principal()
                        sleep(5)
                        try:
                            janela_licenca.destroy()
                        except:
                            pass
                    elif mensagem == "Usuário não encontrado":
                        bttn_ativar_licenca.configure(state="normal")
                        return message_erro("Ocorreu um erro, tente repetir o processo")
                    elif mensagem == "Licença inválida ou já usada":
                        bttn_ativar_licenca.configure(state="normal")
                        return message_erro("Licença inválida ou já usada")
                else:
                    bttn_ativar_licenca.configure(state="normal")
                    return message_erro("Você inseriu uma licença inválida")

            except Exception as e:
                bttn_ativar_licenca.configure(state="normal")
                return message_erro("Ocorreu um erro inesperado!")

        elif mensagem == 'MAC address incorreto!':
            apagar_campos()
            bttn_ativar_licenca.configure(state="normal")
            return message_erro("Esse usuário está cadastrado em outro endereço")
        elif mensagem == 'Senha incorreta!':
            apagar_campos()
            bttn_ativar_licenca.configure(state="normal")
            return message_erro("Esse usuário está cadastrado em outro endereço")
        else:
            apagar_campos()
            message_erro("Você inseriu uma licença inválida")
            return bttn_ativar_licenca.configure(state="normal")

    def iniciar_verificacao():
        threading.Thread(target=verify_licenca).start()
        bttn_ativar_licenca.configure(state="disabled")

    bttn_ativar_licenca = ctk.CTkButton(
        janela_licenca, text="Ativar Licença", command=iniciar_verificacao, width=200, height=40)
    bttn_ativar_licenca.pack(padx=10, pady=5)

    janela_licenca.mainloop()


def app_principal():
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.resizable(False, False)
    janela.title("ToProfit - Cassinos")

    # Frame da barra lateral (sidebar)
    sidebar_frame = ctk.CTkFrame(
        master=janela, width=100, height=600, corner_radius=0)
    sidebar_frame.grid(row=0, column=0, sticky="ns")

    # Frame principal (main_view) onde os outros frames serão exibidos
    main_view = ctk.CTkFrame(master=janela, width=700,
                             height=600, corner_radius=0)
    main_view.grid(row=0, column=1, sticky="ns")

    # Texto inicial do programa
    texto = ctk.CTkLabel(main_view, text="ToProfit - Casa de Apostas",
                         anchor="nw", font=("arial bold", 26))
    texto.grid(row=0, column=1, sticky="n")
    # Frames
    button_group_frame = ctk.CTkFrame(
        master=main_view, width=700, fg_color='transparent', height=600, corner_radius=0)
    button_group_frame.grid(row=1, column=1, sticky="nsew")

    conta_frame = ctk.CTkFrame(
        master=main_view, width=700, fg_color='transparent', height=600, corner_radius=0)
    conta_frame.grid(row=1, column=1, sticky="nsew")

    ajustes_frame = ctk.CTkFrame(
        master=main_view, width=700, fg_color='transparent', height=600, corner_radius=0)
    ajustes_frame.grid(row=1, column=1, sticky="nsew")

    telas_frame = ctk.CTkFrame(
        master=main_view, width=700, fg_color='transparent', height=600, corner_radius=0)
    telas_frame.grid(row=1, column=1, sticky="nsew")

    def show_frame(frame, button):
        button_button_group.configure(fg_color="transparent")
        button_ajustes.configure(fg_color="transparent")
        button_telas.configure(fg_color="transparent")
        button_conta.configure(fg_color="transparent")

        button.configure(fg_color="#206AA5")
        frame.tkraise()

    # Botões do Sidebar
    button_button_group = ctk.CTkButton(master=sidebar_frame, text="Botões", fg_color="transparent",
                                        font=("Arial Bold", 14), hover_color="#206AA5", anchor="w",
                                        width=100, command=lambda: show_frame(button_group_frame, button_button_group))
    button_button_group.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

    button_ajustes = ctk.CTkButton(master=sidebar_frame, text="Ajustes", fg_color="transparent",
                                   font=("Arial Bold", 14), hover_color="#206AA5", anchor="w",
                                   width=100, command=lambda: show_frame(ajustes_frame, button_ajustes))
    button_ajustes.grid(row=1, column=0, sticky="ew", pady=10, padx=10)

    button_telas = ctk.CTkButton(master=sidebar_frame, text="Telas", fg_color="transparent",
                                 font=("Arial Bold", 14), hover_color="#206AA5", anchor="w",
                                 width=100, command=lambda: show_frame(telas_frame, button_telas))
    button_telas.grid(row=2, column=0, sticky="ew", pady=10, padx=10)

    button_conta = ctk.CTkButton(master=sidebar_frame, text="Conta", fg_color="transparent",
                                 font=("Arial Bold", 14), hover_color="#206AA5", anchor="w",
                                 width=100, command=lambda: show_frame(conta_frame, button_conta))
    button_conta.grid(row=3, column=0, sticky="ew", pady=10, padx=10)

    list_games = []

    # Define o caminho para o diretório "Program Files"
    caminho_documents = os.path.join(os.environ['USERPROFILE'], 'Documents')

    # Cria o caminho completo para a pasta principal e para a pasta proxy
    caminho_pasta_principal = os.path.join(caminho_documents, 'To Profit')
    caminho_pasta_proxy = os.path.join(caminho_pasta_principal, "proxy")
    caminho_pasta_extensao = os.path.join(caminho_pasta_principal, "Extensao")
    caminho_cfg = os.path.join(caminho_pasta_principal, "cfg.txt")

    # Cria a pasta principal
    if not os.path.exists(caminho_pasta_principal):
        os.makedirs(caminho_pasta_principal)
    # Cria a pasta proxy dentro da pasta principal
    if not os.path.exists(caminho_pasta_proxy):
        os.makedirs(caminho_pasta_proxy)
    # Cria a pasta proxy dentro da pasta principal
    if not os.path.exists(caminho_pasta_extensao):
        os.makedirs(caminho_pasta_extensao)

    # Textos dentro Variáveis
    vartxt_val_max = None
    vartxt_val_min = None
    vartxt_senha_padrao = None
    vartxt_senha_saque = None
    vartxt_site = None
    bool_checkbox_mobile = ctk.BooleanVar(value=True)
    bool_checkbox_ecoproxy = ctk.BooleanVar(value=True)
    bool_checkbox_senha_rand = ctk.BooleanVar(value=True)
    bool_checkbox_senha_saque_random = ctk.BooleanVar(value=True)
    bool_checkbox_tempoCriacao_rand = ctk.BooleanVar(value=True)
    bool_checkbox_usuarioNumero_rand = ctk.BooleanVar(value=True)

    
    if os.path.exists(caminho_cfg):
        with open(caminho_cfg, 'r') as arquivo:
            conteudo = arquivo.read()

        # Divide o conteúdo por ';'
        parametros = conteudo.split(';')

        # Procura por 'valor_max=' em cada item
        for param in parametros:
            if 'valor_max=' in param:
                # Extrai o valor após o '='
                valor_max = param.split('=')[1]
                if valor_max != " " and valor_max != "":
                    vartxt_val_max = ctk.StringVar(value=valor_max)
            elif 'valor_min=' in param:
                # Extrai o valor após o '='
                valor_min = param.split('=')[1]
                if valor_min != " " and valor_min != "":
                    vartxt_val_min = ctk.StringVar(value=valor_min)
            elif 'jogos=' in param:
                # Extrai o valor após o '='
                jogos = param.split('=')[1]
                if jogos != " " and jogos != "":
                    jogos = jogos.replace(
                        "]", "").replace("[", "").replace("'", "")
                    jogos = jogos.split(",")
                    list_games = list(jogos)
                    try:
                        list_games.remove("")
                    except:
                        pass
                    try:
                        list_games.remove(",")
                    except:
                        pass
                    list_games = [jogo.lstrip() for jogo in list_games]

            elif 'senha_saque=' in param:
                # Extrai o valor após o '='
                senha_saque = param.split('=')[1]
                if senha_saque != " " and senha_saque != "":
                    vartxt_senha_saque = ctk.StringVar(value=senha_saque)
            elif 'senha_padrao=' in param:
                # Extrai o valor após o '='
                senha_padrao = param.split('=')[1]
                if senha_padrao != " " and senha_padrao != "":
                    vartxt_senha_padrao = ctk.StringVar(value=senha_padrao)
            elif 'site=' in param:
                # Extrai o valor após o '='
                site = param.replace("site=", "")
                if site != " " and site != "":
                    vartxt_site = ctk.StringVar(value=site)
            elif 'qdt_loop=' in param:
                qdt_loop = param.replace("qdt_loop=", "")
                
            elif 'modelo_pix=' in param:
                modelo_pix = param.replace("modelo_pix=", "")
            elif 'type_house=' in param:
                type_house = param.replace("type_house=", "")
            elif 'mobile=' in param:
                mobile = param.split('=')[1]
                if mobile != " " and mobile != "":
                    if mobile == "True" or mobile == True:
                        bool_checkbox_mobile = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_mobile = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_mobile = ctk.BooleanVar(value=True)
            
            elif 'ecoproxy=' in param:
                ecoproxy = param.split('=')[1]
                if ecoproxy != " " and ecoproxy != "":
                    if ecoproxy == "True" or ecoproxy == True:
                        bool_checkbox_ecoproxy = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_ecoproxy = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_ecoproxy = ctk.BooleanVar(value=True)
                
            elif 'tempoCriacao_rand=' in param:
                tempoCriacao_rand = param.split('=')[1]
                if tempoCriacao_rand != " " and tempoCriacao_rand != "":
                    if tempoCriacao_rand == "True" or tempoCriacao_rand == True:
                        bool_checkbox_tempoCriacao_rand = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_tempoCriacao_rand = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_tempoCriacao_rand = ctk.BooleanVar(value=True)
            elif 'senha_rand=' in param:
                senha_rand = param.split('=')[1]
                if senha_rand != " " and senha_rand != "":
                    if senha_rand == "True" or senha_rand == True:
                        bool_checkbox_senha_rand = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_senha_rand = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_senha_rand = ctk.BooleanVar(value=True)
            elif 'senha_saque_random=' in param:
                senha_saque_random = param.split('=')[1]
                if senha_saque_random != " " and senha_saque_random != "":
                    if senha_saque_random == "True" or senha_saque_random == True:
                        bool_checkbox_senha_saque_random = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_senha_saque_random = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_senha_saque_random = ctk.BooleanVar(value=True)
                    
            elif 'usuarioNumero_rand=' in param:
                usuarioNumero_rand = param.split('=')[1]
                if usuarioNumero_rand != " " and usuarioNumero_rand != "":
                    if usuarioNumero_rand == "True" or usuarioNumero_rand == True:
                        bool_checkbox_usuarioNumero_rand = ctk.BooleanVar(value=True)
                    else:
                        bool_checkbox_usuarioNumero_rand = ctk.BooleanVar(value=False)
                else:
                    bool_checkbox_usuarioNumero_rand = ctk.BooleanVar(value=True)
                    
    else:
        with open(caminho_cfg, 'w') as arquivo:
            conteudo = f"jogos= ;valor_max= ;valor_min= ;senha_saque= ;senha_padrao= ;site= ;qdt_loop= ;type_house= ;modelo_pix= ;usuarioNumero_rand= ;senha_saque_random= ;senha_rand= ;tempoCriacao_rand= ;mobile= ;ecoproxy= "

            # Escreve o conteúdo no arquivo
            arquivo.write(conteudo)

    threads = []
    abas = []
    senha_criada = False
    # Função para selecionar a planilha

    # Guardando o caminho do documento pessoal
    var_caminho_planilha = ctk.StringVar(value="Planilha Base")

    def gerar_numero_telefone():
        ddd = random.choice([
            11, 12, 13, 14, 15, 16, 17, 18, 19,  # SP
            21, 22, 24,  # RJ
            27, 28,  # ES
            31, 32, 33, 34, 35, 37, 38,  # MG
            41, 42, 43, 44, 45, 46,  # PR
            47, 48, 49,  # SC
            51, 53, 54, 55,  # RS
            61,  # DF
            62, 64,  # GO
            63,  # TO
            65, 66,  # MT
            67,  # MS
            68,  # AC
            69,  # RO
            71, 73, 74, 75, 77,  # BA
            79,  # SE
            81, 82, 83, 84, 85, 86, 87, 88, 89,  # Nordeste
            91, 92, 93, 94, 95, 96, 97, 98, 99  # Norte
        ])

        numero = f'{random.randint(90000, 99999)}-{random.randint(1000, 9999)}'
        return f'{ddd}{numero}'

    def gerar_palavra_aleatoria():
        palavras = [
            # 60% Sobrenomes brasileiros
            'silva', 'santos', 'oliveira', 'pereira', 'costa', 'rodrigues', 'martins', 'junior', 'fernandes', 'souza',
            'almeida', 'lima', 'gomes', 'ribeiro', 'mendes', 'barros', 'cardoso', 'teixeira', 'araujo', 'campos',
            'moraes', 'barbosa', 'freitas', 'pires', 'andrade', 'dias', 'marques', 'carvalho', 'ramos', 'figueiredo',
            'pires', 'reis', 'miranda', 'santiago', 'nunes', 'coelho', 'pinto', 'maciel', 'ferreira', 'cardoso',
            'nogueira', 'vieira', 'monteiro', 'sales', 'ferraz', 'batista', 'simoes', 'duarte', 'moura', 'rocha',
            'melo', 'castro', 'leite', 'baptista', 'campos', 'braga', 'assis', 'farias', 'dantas', 'borges',
            # 20% Sobrenomes de outros países
            'smith', 'johnson', 'brown', 'jones', 'miller', 'davis', 'garcia', 'rodriguez', 'martinez', 'hernandez',
            'lopez', 'gonzalez', 'wilson', 'anderson', 'thomas', 'taylor', 'moore', 'jackson', 'martin', 'lee',
            # 20% Palavras aleatórias
            'fire', 'storm', 'sky', 'hunter', 'shadow', 'river', 'moon', 'star', 'forest', 'wolf',
            'dragon', 'phoenix', 'blade', 'knight', 'ghost', 'dark', 'light', 'wind', 'thunder', 'flame',
            'ice', 'snow', 'rain', 'stone', 'earth', 'mountain', 'sea', 'ocean', 'wave', 'sun',
            'cloud', 'magic', 'spirit', 'hawk', 'falcon', 'eagle', 'lion', 'tiger', 'bear', 'fox', '777',
            'onyx', 'pearl', 'ruby', 'sapphire', 'emerald', 'diamond', 'topaz', 'jade', 'king', 'divine', 'slots', 'beats', 'slotszin'
        ]
        return random.choice(palavras)

    def gerar_usuarios(nome):
        alfabeto = 'abcdefghijklmnopqrstuvwxyz'
        nome = nome.lower()  # Transformar o nome em minúsculas
        nome = unidecode(nome)

        while True:
            quantidade_digitos = random.randint(2, 4)
            numero = ''.join(str(random.randint(0, 9))
                             for _ in range(quantidade_digitos))

            # Adicionar palavra aleatória (simulada aqui com um exemplo fixo)
            adicionar_palavra = random.choice([True, False])
            palavra_aleatoria = gerar_palavra_aleatoria(
            ) if adicionar_palavra else ''  # Exemplo de palavra aleatória

            nome_partes = nome.split()
            if len(nome_partes) > 1:
                nome1 = random.choice(nome_partes)
            else:
                nome1 = nome

            # Criar diferentes variações do nome
            variacoes = [
                nome + str(numero),
                str(numero) + nome,
                nome + palavra_aleatoria,
                palavra_aleatoria + nome + str(numero),
                nome + numero + random.choice(alfabeto),
                palavra_aleatoria + random.choice(alfabeto) + str(numero),
                str(numero) + palavra_aleatoria,
                palavra_aleatoria +
                ''.join(random.choice(alfabeto) for _ in range(3)),
                nome1.replace("o", "0") + str(numero),
                nome.replace("o", "0") + str(numero),
                nome1.replace("a", "4") + str(numero),
                nome.replace("a", "4") + str(numero),
                palavra_aleatoria.replace("o", "0") + str(numero),
                palavra_aleatoria.replace("a", "4") + str(numero),
                nome1.replace("o", "0") + random.choice(alfabeto) +
                random.choice(alfabeto),
                nome.replace("o", "0") + random.choice(alfabeto) +
                random.choice(alfabeto),
                palavra_aleatoria.replace(
                    "o", "0") + random.choice(alfabeto) + random.choice(alfabeto),
                nome1.replace("a", "4") + random.choice(alfabeto) +
                random.choice(alfabeto)
            ]

            # Selecionar aleatoriamente uma das variações
            usuario = random.choice(variacoes)

            # Verificar se o usuário gerado tem entre 5 e 15 caracteres
            if 5 <= len(usuario) <= 15:
                usuario_proibido = numero + nome
                usuario_proibido1 = nome + numero

                if usuario not in [usuario_proibido, usuario_proibido1, nome, nome1]:
                    return usuario

    def apagar_zips():
        # Verifica se a pasta existe
        if os.path.exists(caminho_pasta_proxy):
            # Lista todos os arquivos dentro da pasta
            for arquivo in os.listdir(caminho_pasta_proxy):
                caminho_arquivo = os.path.join(caminho_pasta_proxy, arquivo)
                # Verifica se o arquivo é um arquivo zip
                if arquivo.endswith('.zip'):
                    # Apaga o arquivo zip
                    os.remove(caminho_arquivo)

    def consultar_txt():
        if os.path.exists(caminho_cfg):
            with open(caminho_cfg, 'r') as arquivo:
                conteudo = arquivo.read()

            # Divide o conteúdo por ';'
            parametros = conteudo.split(';')

            # Procura por 'valor_max=' em cada item
            for param in parametros:
                if 'valor_max=' in param:
                    # Extrai o valor após o '='
                    valor_max = param.split('=')[1]
                    vartxt_val_max = ctk.StringVar(value=valor_max)
                elif 'valor_min=' in param:
                    # Extrai o valor após o '='
                    valor_min = param.split('=')[1]
                    vartxt_val_min = ctk.StringVar(value=valor_max)
                elif 'jogos=' in param:
                    # Extrai o valor após o '='
                    jogos = param.split('=')[1]
                    list_games = list(jogos)
                elif 'senha_saque=' in param:
                    # Extrai o valor após o '='
                    senha_saque = param.split('=')[1]
                    vartxt_senha_saque = ctk.StringVar(value=senha_saque)
                elif 'senha_padrao=' in param:
                    # Extrai o valor após o '='
                    senha_padrao = param.split('=')[1]
                    vartxt_senha_padrao = ctk.StringVar(value=senha_padrao)
                elif 'site=' in param:
                    # Extrai o valor após o '='
                    site = param.replace("site=", "")
                    vartxt_site = ctk.StringVar(value=site)
                elif 'qdt_loop=' in param:
                    # Extrai o valor após o '='
                    qdt_loop = param.replace("qdt_loop=", "")
                elif 'modelo_pix=' in param:
                    # Extrai o valor após o '='
                    modelo_pix = param.replace("modelo_pix=", "")
                elif 'type_house=' in param:
                    # Extrai o valor após o '='
                    type_house = param.replace("type_house=", "")
                
        return senha_saque, senha_padrao, valor_max, valor_min, site,qdt_loop,modelo_pix,type_house

    def escolher_planilha():
        global caminho_planilha
        caminho_planilha = filedialog.askopenfilename()
        caminho_planilha_format = caminho_planilha.split("/")[-1].strip()

        try:
            if caminho_planilha:
                caminho_planilha_final = caminho_planilha[-5:]
                if caminho_planilha_final == ".xlsx" or ".xls" in caminho_planilha_final or caminho_planilha_final == ".xlsm" or caminho_planilha_final == ".xlsb" or caminho_planilha_final == ".xltx":
                    pass
                elif caminho_planilha_final == "" or caminho_planilha_final == " ":
                    message_erro("Você não inseriu uma planilha excel")
                    return
                else:
                    message_erro("Você inseriu uma planilha inválida")
                    return
        except:
            message_erro("Você não inseriu nenhuma planilha")
            return

        var_caminho_planilha.set(caminho_planilha_format)

    def gerar_senha_saque_random(tamanho=6):
        senha = []

        while len(senha) < tamanho:
            numero = random.randint(0, 9)

            # Verifica se o número não é consecutivo nem repetido do anterior
            if len(senha) == 0 or (senha[-1] != numero and abs(senha[-1] - numero) > 1):
                senha.append(numero)

        return ''.join(map(str, senha))

    def gerar_senha_random(palavra=None):
        # Define caracteres permitidos (letras e números)
        caracteres = string.ascii_letters + string.digits

        # Função para gerar senha aleatória
        senha = ''.join(random.choice(caracteres) for _ in range(12))

        # Se uma palavra foi fornecida e de forma aleatória (de acordo com a chance), insira na senha
        if palavra and random.random() < 0.3:
            posicao_inserir = random.randint(0, len(senha) - len(palavra))
            senha = senha[:posicao_inserir] + palavra + \
                senha[posicao_inserir + len(palavra):]

        return senha

    def random_user_agent_mobile():
        dispositivos = [
            {"deviceName": "iPhone X",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15A5341f Safari/604.1"},
            {"deviceName": "Pixel 2",
                "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"},
            {"deviceName": "Samsung Galaxy S9+",
                "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G965F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"},
            {"deviceName": "iPhone 12 Pro",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A5341f Safari/604.1"},
            {"deviceName": "Pixel 4",
                "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 4 Build/QQ3A.200805.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36"},
            {"deviceName": "iPhone 11",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1"},
            {"deviceName": "Samsung Galaxy Note 10",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-N970F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36"},
            {"deviceName": "OnePlus 7T",
                "userAgent": "Mozilla/5.0 (Linux; Android 10; HD1901) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36"},
            {"deviceName": "Huawei P30 Pro",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"},
            {"deviceName": "Xiaomi Mi 9",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; Mi 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"},
            {"deviceName": "iPhone SE",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1"},
            {"deviceName": "Samsung Galaxy S10",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-G973F Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36"},
            {"deviceName": "iPhone 8",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"},
            {"deviceName": "Google Nexus 5",
                "userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.105 Mobile Safari/537.36"},
            {"deviceName": "Motorola Moto G7",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36"},
            {"deviceName": "iPhone 6S",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"},
            {"deviceName": "Samsung Galaxy A50",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"},
            {"deviceName": "Sony Xperia XZ2",
                "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; H8216 Build/41.3.A.0.401) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36"},
            {"deviceName": "iPhone 7",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A346 Safari/602.1"},
            {"deviceName": "Google Pixel XL",
                "userAgent": "Mozilla/5.0 (Linux; Android 7.1.2; Pixel XL Build/NKG47L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36"},
            {"deviceName": "Huawei Mate 20 Pro",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; LYA-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.90 Mobile Safari/537.36"},
            {"deviceName": "iPhone XR",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"},
            {"deviceName": "Samsung Galaxy S8",
                "userAgent": "Mozilla/5.0 (Linux; Android 7.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"},
            {"deviceName": "OnePlus 6",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"},
            {"deviceName": "Xiaomi Redmi Note 8",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"},
            {"deviceName": "iPhone 13 Pro",
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},
            {"deviceName": "Samsung Galaxy Z Fold3",
                "userAgent": "Mozilla/5.0 (Linux; Android 11; SM-F926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"},
            {"deviceName": "LG G7 ThinQ",
                "userAgent": "Mozilla/5.0 (Linux; Android 8.0.0; LM-G710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36"},
            {"deviceName": "Motorola Edge+",
                "userAgent": "Mozilla/5.0 (Linux; Android 10; motorola edge plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36"},
            {"deviceName": "Nokia 7.2",
                "userAgent": "Mozilla/5.0 (Linux; Android 9; Nokia 7.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36"}
        ]

        # Escolhe um dispositivo aleatório da lista
        dispositivo_aleatorio = random.choice(dispositivos)

        # Retorna o nome do dispositivo e o user agent
        return dispositivo_aleatorio["deviceName"], dispositivo_aleatorio["userAgent"]

    # Função para gerar um user-Agent aleatorio
    def random_user_agent_pc():

        user_agents_pc = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
        ]

        return random.choice(user_agents_pc)

    # Função para gerar uma platform aleatória
    def random_platform():
        platforms = [
            "Win32",
            "Win64",
            "Linux x86_64",
            "Linux i686",
            "X11"
        ]
        return random.choice(platforms)

    # Função para gerar uma memória aleatória
    def random_memory():
        memory = ["2GB", "4GB", "8GB", "16GB"]
        return random.choice(memory)

    # Função para gerar uma Webgl aleatório
    def random_webgl_vendor():
        vendors = ["Intel Inc.", "NVIDIA Corporation", "AMD Inc."]
        return random.choice(vendors)

    # Função para gerar um renderer aleatório
    def random_renderer(vendor):
        renderers = {
            "Intel Inc.": ["Intel Iris OpenGL Engine", "Intel HD Graphics 4000"],
            "NVIDIA Corporation": ["NVIDIA GeForce GTX 1050 Ti OpenGL Engine", "NVIDIA GeForce GTX 1080 Ti OpenGL Engine"],
            "AMD Inc.": ["AMD Radeon Pro 580 OpenGL Engine", "AMD Radeon RX 580 OpenGL Engine"]
        }
        return random.choice(renderers[vendor])

    def criar_extensao_com_dados(dados_navegador):
        usuario = dados_navegador["usuario"]
        posicao = dados_navegador["posicao_janela"]
        senha = dados_navegador["senha"]
        cpf = dados_navegador["cpf"]
        senha_saque = dados_navegador["senha_saque"]

        # Manifesto da extensão
        manifest_json = '''
        {
            "manifest_version": 2,
            "name": "Exibir Dados Específicos",
            "version": "1.0",
            "description": "Uma extensão que mostra os dados de senha, usuário, número da tela, CPF e senha de saque.",
            "browser_action": {
                "default_popup": "popup.html",
                "default_title": "Mostrar Dados"
            },
            "permissions": [
                "storage"
            ],
            "background": {
                "scripts": ["background.js"],
                "persistent": false
            }
        }
        '''

        # Cria o arquivo popup.html
        popup_html = '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Exibir Dados</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 10px;
                }
                .container {
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <strong>Usuário:</strong> <span id="usuario"></span>
            </div>
            <div class="container">
                <strong>Senha:</strong> <span id="senha"></span>
            </div>
            <div class="container">
                <strong>Número da Tela:</strong> <span id="numero_tela"></span>
            </div>
            <div class="container">
                <strong>CPF:</strong> <span id="cpf"></span>
            </div>
            <div class="container">
                <strong>Senha de Saque:</strong> <span id="senha_saque"></span>
            </div>

            <script src="popup.js"></script>
        </body>
        </html>
        '''

        # Cria o arquivo popup.js
        popup_js = '''
        document.addEventListener('DOMContentLoaded', function () {
            chrome.storage.local.get(['usuario', 'senha', 'numero_tela', 'cpf', 'senha_saque'], function (result) {
                console.log("Dados recuperados do storage:", result);

                // Exibe os dados no popup
                document.getElementById('usuario').textContent = result.usuario;
                document.getElementById('senha').textContent = result.senha;
                document.getElementById('numero_tela').textContent = result.numero_tela;
                document.getElementById('cpf').textContent = result.cpf;
                document.getElementById('senha_saque').textContent = result.senha_saque;
            });
        });
        '''

        # Armazena os dados no storage quando a extensão é instalada
        background_js = f'''
        chrome.runtime.onInstalled.addListener(function() {{
            chrome.storage.local.set({{
                'usuario': "{usuario}",
                'senha': "{senha}",
                'numero_tela': "{posicao}",
                'cpf': "{cpf}",
                'senha_saque': "{senha_saque}"
            }}, function() {{
                console.log("Dados armazenados com sucesso:", {{
                    usuario: "{usuario}",
                    senha: "{senha}",
                    numero_tela: "{posicao}",
                    cpf: "{cpf}",
                    senha_saque: "{senha_saque}"
                }});
            }});
        }});
        '''

        # Criação do arquivo ZIP da extensão no local especificado
        pluginfile = os.path.join(
            caminho_pasta_extensao, f'proxy_extensao{posicao}.zip')

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("popup.html", popup_html)
            zp.writestr("popup.js", popup_js)
            zp.writestr("background.js", background_js)

        return pluginfile

    # Função para gerar um chromedriver com Proxys e carregar a extensão com dados específicos
    def create_chromedriver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, pos_x, pos_y, altura, largura, posicao, dados_navegador):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
        );

        chrome.webRequest.onBeforeSendHeaders.addListener(
            function(details) {
                for (var i = 0; i < details.requestHeaders.length; ++i) {
                    if (details.requestHeaders[i].name === 'Accept-Language') {
                        details.requestHeaders[i].value = 'pt-BR,pt;q=0.9';
                        break;
                    }
                }
                return {requestHeaders: details.requestHeaders};
            },
            {urls: ["<all_urls>"]},
            ["blocking", "requestHeaders"]
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        def get_chromedriver(use_proxy=True, x=pos_x, y=pos_y, alt=altura, larg=largura, posicao_janela=posicao):
            path = os.path.dirname(os.path.abspath(__file__))
            chrome_options = Options()

            if use_proxy:
                pluginfile = os.path.join(
                    caminho_pasta_proxy, f'proxy_{posicao_janela}.zip')
                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            pluginfile_extensao = criar_extensao_com_dados(dados_navegador)
            chrome_options.add_extension(pluginfile_extensao)

            if bool_checkbox_ecoproxy.get():

                prefs = {
                    "profile.default_content_setting_values": {
                        "plugins": 2  # Disable plugins (videos, audio)
                    },
                    'intl.accept_languages': 'pt-BR,pt',
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": True
                }
                chrome_options.add_experimental_option("prefs", prefs)
                chrome_options.add_argument("disk-cache-size=4096")
                chrome_options.add_argument('--disable-application-cache')

            else:
                chrome_options.add_experimental_option('prefs', {
                    'intl.accept_languages': 'pt-BR,pt',
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": True
                })

            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"])

            if bool_checkbox_mobile.get():
                user_agent, devicename = random_user_agent_mobile()

                arguments = [f'user-agent={user_agent}', '--mute-audio',
                             f"--window-position={x},{y}", f"--window-size={larg},{alt}"]

            else:
                user_agent = random_user_agent_pc()
                arguments = [f'user-agent={user_agent}', '--mute-audio',
                             f"--window-position={x},{y}", f"--window-size={larg},{alt}"]

            for argument in arguments:
                chrome_options.add_argument(argument)

            driver = webdriver.Chrome(options=chrome_options)
            return driver

        driver = get_chromedriver(use_proxy=True)

        # Stealth Apagar

        webgl_vendor = random_webgl_vendor()
        renderer = random_renderer(webgl_vendor)

        stealth(driver,
                languages=["pt-BR", "pt"],
                vendor="Google Inc.",
                platform=random_platform(),
                webgl_vendor=webgl_vendor,
                renderer=renderer,
                fix_hairline=True,
                run_on_insecure_content=True,
                do_not_track=1
                )

        return driver

    # Remover abas abertas
    def verificar_e_remover_abas_fechadas():
        abas_ativas = []
        for dados_navegador in abas:
            try:
                chrome = dados_navegador["driver"]
                chrome.title  # Tenta acessar a propriedade title para verificar se o navegador está ativo

                abas_ativas.append(dados_navegador)
            except:
                pass  # Se o navegador foi fechado, ele não é adicionado à lista de abas ativas
        return abas_ativas

    # Função para formatar uma proxy
    def formatar_proxy(proxy):
        myproxy = proxy.split(":")

        proxy_host = myproxy[0]
        proxy_port = myproxy[1]
        proxy_user = myproxy[2]
        proxy_pass = myproxy[3]

        return proxy_host, proxy_port, proxy_user, proxy_pass

    def calcula_digito(digs):
        s = 0
        qtd = len(digs)
        for i in range(qtd):
            s += digs[i] * (1 + qtd - i)
        res = 11 - s % 11
        if res > 9:
            return 0
        else:
            return res

    # Função para gerar um CPF
    def gerar_cpf():
        # Gerar os nove primeiros dígitos de forma aleatória
        n = [random.randint(0, 9) for _ in range(9)]

        # Calcular o primeiro dígito verificador
        d1 = calcula_digito(n)
        n.append(d1)

        # Calcular o segundo dígito verificador
        d2 = calcula_digito(n)
        n.append(d2)

        # Converter os números para string e formatar
        return f"{n[0]}{n[1]}{n[2]}.{n[3]}{n[4]}{n[5]}.{n[6]}{n[7]}{n[8]}-{n[9]}{n[10]}"

    # Funcao para alterar as URLS
    def modificar_url(link, novo_caminho, nova_query):
        parsed_url = urlparse(link)

        # Cria uma nova URL com o novo caminho (/home/withdraw)e nova query (sem a ?...)
        if nova_query != "nenhum":
            nova_url = parsed_url._replace(path=novo_caminho, query=nova_query)
        else:
            nova_url = parsed_url._replace(path=novo_caminho)
        nova_url_completa = urlunparse(nova_url)

        return nova_url_completa

    # Funcao para verificar a quantidade de 2 pontos da proxy.
    def verificar_pontos(string):
        minha_string = string
        # Use o método count() para contar o número de ocorrências de ':'
        qntd_de_dois_pontos = minha_string.count(':')
        return qntd_de_dois_pontos

    # Funcao para fechar avisos
    def fechar_avisos(chrome):
        try:
            warn = chrome.find_element(
                By.XPATH, "//div[@class='ant-modal-confirm-btns']")
            warn.find_element(
                By.XPATH, "//button[@type='button' and @class='ant-btn ant-btn-default']").click()
        except:
            pass
        try:
            chrome.find_element(
                By.XPATH, "//input[@type='checkbox' and @class='ant-checkbox-input']").click()
        except:
            pass

    def iniciar_navegadores():
        global caminho_planilha
        qtd_loop = options_qtd_loop.get()
        qtd_loop = int(qtd_loop)

        if not os.path.exists("Usuarios.txt"):
            # Abre o arquivo no modo 'w' para escrita
            with open("Usuarios.txt", 'w') as arquivo:
                conteudo = f"NOME UNICO - USUARIO - SENHA - SENHA SAQUE ----- PROXY ---- SITE - DATA\n"
                # Escreve o conteúdo no arquivo
                arquivo.write(conteudo)

        # Carregar planilha
        try:
            df = pd.read_excel(caminho_planilha)
            # Convertendo a coluna 'STATUS' para tipo object
            df['STATUS'] = df['STATUS'].astype('object')
            # Assegura que a coluna 'DATA_HORARIO' pode receber strings
            df['DATA_HORARIO'] = df['DATA_HORARIO'].astype('object')

            if not all(coluna in df.columns for coluna in ["PROXY", "STATUS"]):
                message_erro(
                    "A planilha não contém todas as colunas desejadas.")
                return
        except Exception as e:
            message_erro(f"Não foi possível ler esta planilha: {str(e)}")
            return

        navegadores = []
        site_dig = entry_site.get()
        posicao_janela = 0

        try:
            jogo_atual = dropbox_games.get()
            mac = obter_endereco_mac()
            url_desc_game = "https://script.google.com/macros/s/AKfycbxUST8kEp1xVakdqBK0CxtfCYc-sCEX665mKRwXpqBUvR0fO8Ig_PMnB0JSomJLhYomGg/exec"

            horario = datetime.now().isoformat()

            dados = {
                'mac_address': mac,
                'site': site_dig,
                'jogo': jogo_atual,
                'horario': horario,
                'telas': qtd_loop
            }

            requests.post(url=url_desc_game, json=dados)
        except:
            pass

        # Filtra as linhas onde STATUS é NaN e limita a quantidade de linhas a processar
        for index, row in df[df['STATUS'].isna()].head(qtd_loop).iterrows():
            posicao_janela += 1
            try:
                proxy = row.get("PROXY")
            except KeyError as e:
                message_erro(
                    f"A coluna Proxy tem linhas que não estão completas: {e}")
                return
            try:
                site = row.get("SITE")
            except:
                pass
            try:
                usuario = row.get("USUARIO")
            except:
                pass

            dados_navegador = {
                "site": site_dig if site_dig != "" and not " " in site_dig else site,
                "usuario": usuario,
                "proxy": proxy,
                "index": index,
                "posicao_janela": posicao_janela  # Adiciona a posição da janela ao dicionário
            }

            navegadores.append(dados_navegador)

            # Obtendo a data e hora atuais
            agora = datetime.now()
            df.at[index, 'DATA_HORARIO'] = agora.strftime(
                "%Y-%m-%d %H:%M:%S")  # Formata como 'AAAA-MM-DD HH:MM:SS'

        apagar_zips()

        # Loop para automatizar os sites
        for navegador in navegadores:
            # Envia o dicionário como um único argumento
            iniciar_abrir_navegador(navegador)
            if navegador["posicao_janela"] == qtd_loop:
                break

        acesso, mensagem = consultar_permissao_computador()
        if acesso == True:
            pass
        elif acesso == False:
            message_erro(
                f"Você não tem permissão para usar o App:\n {mensagem}")
            sleep(5)
            return janela.destroy()

        # Atualizando o STATUS para 'USADO'
        df.loc[[navegador["index"]
                for navegador in navegadores], 'STATUS'] = 'USADO'
        df.to_excel(caminho_planilha, index=False)
    def gerar_nomesPrimarios():
        lista_nomes_unicos = [
            "Adalberto", "Adalgisa", "Adão", "Adela", "Adelaide", "Adelberto", "Adèle", "Adélia", "Adelina", "Ademar", 
            "Adhemar", "Adolfo", "Adolpho", "Adrian", "Adriana", "Adriane", "Adrianne", "Adriano", "Adriene", "Adrienne", 
            "Afonso", "Ágata", "Agatha", "Agenor", "Agnaldo", "Agnes", "Agostinho", "Aguinaldo", "Aída", "Aiko", "Aílton", 
            "Aimée", "Airton", "Ajit", "Akahana", "Akako", "Alaíde", "Alana", "Alane", "Alanna", "Alanne", "Alba", "Alberta", 
            "Albertina", "Alberto", "Alceu", "Alcides", "Alcione", "Alcyone", "Alda", "Aldaberto", "Aldine", "Aldo", "Alec", 
            "Alecsandra", "Alegra", "Alejandra", "Aleksandra", "Alessandra", "Alessandro", "Alex", "Alexandra", "Alexandre", 
            "Aléxis", "Alfonso", "Alfredo", "Alice", "Alicia", "Alisha", "Allegra", "Aloísio", "Alonso", "Aluísio", "Álvaro", 
            "Alzira", "Amadeu", "Amadeus", "Amália", "Amanda", "Amar", "Amauri", "Amaury", "Amedeo", "Amélia", "Amélie", 
            "América", "Américo", "Amílcar", "Amisha", "Amita", "Amiti", "Amy", "Ana", "Anaís", "Anastácia", "Anastasia", 
            "André", "Andréa", "Andréia", "Andresa", "Andressa", "Andreza", "Andrezza", "Anete", "Angel", "Ângela", "Angeli", 
            "Angélica", "Angelina", "Angelita", "Ângelo", "Aníbal", "Anísio", "Anita", "Anna", "Anne", "Annete", "Anoush", 
            "Anselmo", "Antenor", "Antonela", "Antonella", "Antônia", "Antonieta", "Antônio", "Aparecida", "Aquiles", "Araci", 
            "Aracy", "Areta", "Aretha", "Ariana", "Ariane", "Ariela", "Ariella", "Arielle", "Arlene", "Arlete", "Armando", 
            "Arnaldo", "Arthur", "Artur", "Asha", "Assunção", "Astrid", "Astride", "Ataúlfo", "Augusta", "Augustina", 
            "Augustine", "Augusto", "Aurélia", "Aurélio", "Auro", "Aurora", "Auxiliadora", "Ayrton", "Ayumi", "Babette", 
            "Balbina", "Balraj", "Baltazar", "Bárbara", "Barbie", "Barbra", "Bartolomeu", "Basílio", "Beata", "Beatrice", 
            "Beatrix", "Beatriz", "Bela", "Belinda", "Bella", "Belle", "Benedicta", "Benedicto", "Benedita", "Benedito", 
            "Benício", "Benito", "Benjamim", "Benjamin", "Bento", "Berenice", "Bernadete", "Bernadette", "Bernarda", 
            "Bernardino", "Bernardo", "Berta", "Bertha", "Betânia", "Bete", "Beth", "Betina", "Bianca", "Biatriz", "Blanche", 
            "Bóris", "Branca", "Brenda", "Breno", "Briana", "Brianne", "Bridget", "Brígida", "Brigite", "Brigitte", "Brione", 
            "Bruna", "Brunete", "Bruno", "Cacilda", "Caetano", "Caio", "Calista", "Calixta", "Calixto", "Camélia", "Camellia", 
            "Cameron", "Camila", "Camile", "Camilla", "Camille", "Camilo", "Candice", "Cândida", "Cândido", "Capitu", 
            "Carina", "Carine", "Carla", "Carlo", "Carlos", "Carlota", "Carmel", "Carmela", "Carmelita", "Carmem", "Carmen", 
            "Carmina", "Carmo", "Carol", "Carola", "Carolina", "Caroline", "Carolyn", "Carolyne", "Cassandra", "Cássia", 
            "Cassiano", "Cassilda", "Cássio", "Catarina", "Caterina", "Catherine", "Cécile", "Cecília", "Celeste", "Célia", 
            "Celina", "Céline", "Célio", "Celso", "Ceres", "César", "Chandra", "Charles", "Charlotte", "Chelsea", "Chiara", 
            "Chloé", "Christal", "Christian", "Christiana", "Christiane", "Christina", "Christopher", "Chrystal", "Cibele", 
            "Cícero", "Cilene", "Cinthia", "Cíntia", "Ciro", "Clair", "Claire", "Clara", "Clarice", "Clarissa", "Clarisse", 
            "Claudete", "Claudette", "Cláudia", "Cláudio", "Cleide", "Clélia", "Cleusa", "Cloé", "Clotilda", "Clotilde", 
            "Clotildes", "Conceição", "Conrado", "Consuelo", "Cora", "Cordélia", "Corina", "Cornélia", "Cosette", "Creusa", 
            "Creuza", "Cristal", "Cristiana", "Cristiane", "Cristiano", "Cristina", "Cristóvão", "Cynthia", "Cyntia", 
            "Dafne", "Dagmar", "Dagmara", "Daiana", "Daiane", "Daisy", "Dália", "Dalila", "Dalton", "Dalva", "Damião", "Dana", 
            "Daniel", "Daniela", "Daniele", "Daniella", "Danielle", "Danilo", "Dante", "Daphne", "Dara", "Darci", "Darcy", 
            "Daria", "Dario", "Darlene", "Davi", "David", "Daya", "Débora", "Deborah", "Décio", "Deepak", "Deise", "Delfina", 
            "Délia", "Demi", "Denice", "Dênis", "Denise", "Desirée", "Deva", "Devi", "Dhara", "Diana", "Diane", "Diego", 
            "Diná", "Dinah", "Diogo", "Dione", "Dionise", "Dipak", "Dirce", "Dirceu", "Diva", "Djalma", "Djane", "Dolores", 
            "Dominique", "Donata", "Dora", "Doralice", "Dóris", "Dorotéa", "Dorotéia", "Dorothy", "Dulce", "Dulcinéa", 
            "Dulcineia", "Éder", "Edgar", "Édison", "Edite", "Edith", "Edmundo", "Edna", "Édson", "Eduardo", "Elaine", "Elba", 
            "Elenice", "Eleonor", "Eleonora", "Eliana", "Eliane", "Elias", "Élio", "Elis", "Elisa", "Elisabete", "Elisabeth", 
            "Eliseu", "Eliza", "Elizabete", "Elizabeth", "Eloá", "Eloah", "Eloísa", "Elsa", "Elvira", "Elvis", "Elza", "Elzira", 
            "Ema", "Emanuel", "Emanuela", "Emanuele", "Emanuelle", "Émerson", "Emília", "Emílio", "Emily", "Emma", "Enrico", 
            "Enrique", "Enzo", "Erasmo", "Eric", "Érica", "Érico", "Érika", "Ériko", "Ernesto", "Esmeralda", "Esperança", 
            "Estéfano", "Estela", "Ester", "Estevão", "Esther", "Eugênia", "Eugênio", "Eunice", "Eva", "Evandro", "Evangelina", 
            "Eve", "Évelin", "Evelina", "Eveline", "Evelyn", "Fábia", "Fabiana", "Fabiano", "Fábio", "Fabíola", "Fabrícia", 
            "Fabrício", "Fabrizio", "Fanny", "Fátima", "Fausta", "Faustina", "Fausto", "Felícia", "Felício", "Felipa", "Felipe", 
            "Félix", "Ferdinando", "Fernanda", "Fernando", "Fernão", "Filipa", "Filipe", "Filippo", "Filomena", "Fiona", 
            "Flávia", "Flávio", "Flor", "Flora", "Franca", "Frances", "Francesca", "Francesco", "Francine", "Francis", 
            "Francisca", "Francisco", "Françoise", "Frederico", "Frida", "Gabriel", "Gabriela", "Gabriele", "Gabriella", 
            "Gabrielle", "Gaetano", "Ganesh", "Genji", "George", "Georgia", "Georgiana", "Georgina", "Geralda", "Geraldo", 
            "Germano", "Gérson", "Gertrude", "Gertrudes", "Gervásio", "Giancarlo", "Gilberto", "Gilda", "Gilmar", "Gilmara", 
            "Gilson", "Gina", "Gioconda", "Giorgio", "Giovana", "Giovanna", "Giovanni", "Gisela", "Giselda", "Gisele", 
            "Gisella", "Giselle", "Gita", "Giulia", "Gizelda", "Gládis", "Gladys", "Gláuber", "Glauce", "Gláucia", "Glauco", 
            "Glenda", "Glória", "Gonçalo", "Gonzalo", "Graça", "Grace", "Graziela", "Gregório", "Greice", "Greta", "Gretchen", 
            "Guálter", "Guilherme", "Guiomar", "Gunther", "Gustavo", "Gyselle", "Hadrián", "Haidê", "Haideé", "Halima", 
            "Hamilton", "Hannah", "Haydê", "Hebe", "Hector", "Heidi", "Heitor", "Helena", "Helenice", "Helga", "Hélio", 
            "Heloísa", "Henrique", "Henriqueta", "Henry", "Herculano", "Hilda", "Hildegard", "Homero", "Horácio", "Horishi", 
            "Hortênsia", "Hugo", "Humberto", "Iara", "Ícaro", "Idalina", "Ieda", "Iemanjá", "Ignácio", "Igor", "Ilsa", "Inácio", 
            "Indra", "Inês", "Inez", "Ingrid", "Íngride", "Iolanda", "Ioná", "Ione", "Iracema", "Irene", "Irina", "Íris", "Isa", 
            "Isaac", "Isabel", "Isabela", "Isabele", "Isabella", "Isabelle", "Isadora", "Isaías", "Isaura", "Isidora", 
            "Isidoro", "Ísis", "Ismael", "Israel", "Ítalo", "Itamar", "Iuri", "Ivã", "Ivan", "Ivete", "Ivette", "Ivo", "Ivone", 
            "Ivonne", "Izabela", "Jaci", "Jacira", "Jacó", "Jacob", "Jacqueline", "Jacques", "Jacy", "Jacyra", "Jade", "Jaime", 
            "Jair", "Jairo", "Jamal", "Jamil", "Jamila", "Janaína", "Jandir", "Jandira", "Jandyr", "Jandyra", "Jane", "Janete", 
            "Janice", "Jaqueline", "Jasmim", "Jasmin", "Jasmina", "Jasmine", "Jean", "Jefferson", "Jeni", "Jenifer", "Jennifer", 
            "Jenny", "Jeremias", "Jéssica", "Jin", "Joana", "Joanna", "João", "Joaquim", "Joaquina", "Joel", "Joelle", "Jonas", 
            "Jonatan", "Jônatas", "Jonathan", "Jordana", "Jordão", "Jorge", "José", "Josefina", "Josephine", "Josias", "Joy", 
            "Juarez", "Judite", "Judith", "Júlia", "Juliana", "Juliano", "Julieta", "Júlio", "Júnior", "Jussara", "Justina", 
            "Justino", "Kaila", "Kaio", "Kalil", "Kalila", "Kaori", "Karen", "Karim", "Karina", "Karine", "Karla", "Karoline", 
            "Kássia", "Kate", "Katerine", "Katharina", "Katherine", "Kátia", "Katya", "Keiko", "Keila", "Keith", "Kelly", 
            "Kelvin", "Késia", "Khalil", "Kim", "Kin", "Kristal", "Kyoko", "Laércio", "Laerte", "Laila", "Lailah", "Laís", 
            "Laísa", "Lana", "Lara", "Larisa", "Larissa", "Lateefah", "Latifa", "Latiffa", "Laura", "Lauro", "Lavínia", 
            "Layla", "Lázaro", "Léa", "Leandra", "Leandro", "Leda", "Léia", "Leila", "Leilah", "Lenora", "Leon", "Leona", 
            "Leonardo", "Leônidas", "Leonor", "Leonora", "Leopoldo", "Letícia", "Letizia", "Li", "Lia", "Lídia", "Lien", 
            "Lígia", "Lila", "Lília", "Lilian", "Liliana", "Liliane", "Lina", "Linda", "Lindsay", "Linete", "Linette", "Lineu", 
            "Lisa", "Lisandra", "Lisandro", "Lívia", "Lívio", "Liza", "Lizandra", "Lizandro", "Lola", "Lorelei", "Lorena", 
            "Lorenzo", "Loreta", "Lourdes", "Lourenço", "Luana", "Luca", "Lucas", "Luci", "Lúcia", "Luciana", "Luciane", 
            "Luciano", "Luciene", "Lucila", "Lúcio", "Lucy", "Ludemila", "Ludmila", "Luigi", "Luís", "Luísa", "Luiz", "Luiza", 
            "Luna", "Lurdes", "Luzia", "Lydia", "Lynn", "Mabel", "Madalena", "Mafalda", "Magali", "Magda", "Magdalena", 
            "Magno", "Maia", "Maiara", "Maíra", "Maísa", "Maitê", "Malika", "Manoel", "Manoela", "Manu", "Manuel", "Manuela", 
            "Manuelle", "Maomé", "Mara", "Marcel", "Marcela", "Marcele", "Marcella", "Marcello", "Marcelo", "Márcia", 
            "Márcio", "Marco", "Marcos", "Margarida", "Margarita", "Margot", "Maria", "Mariah", "Mariana", "Mariângela", 
            "Marianne", "Mariano", "Marília", "Marina", "Mário", "Marisa", "Marise", "Mariza", "Marize", "Marjorie", "Marlene", 
            "Marli", "Marly", "Marta", "Martha", "Martim", "Martina", "Marvin", "Mary", "Masculino", "Mateus", "Matheus", 
            "Mathias", "Matias", "Matilda", "Matilde", "Maura", "Maurício", "Mauro", "Maya", "Mayara", "Mayra", "Maysa", 
            "Megan", "Meire", "Melinda", "Melissa", "Melvin", "Messias", "Micael", "Michaela", "Michaella", "Michel", "Michele", 
            "Michelle", "Midori", "Miguel", "Mika", "Mildred", "Milena", "Milton"
        ]

        nome_escolhido = random.choice(lista_nomes_unicos)
        nome_escolhido = unidecode(nome_escolhido)

        return nome_escolhido
    
    def gerar_sobrenomes():
        lista_sobrenomes = [
            "Silva", "Santos", "Oliveira", "Souza", "Pereira", "Lima", "Carvalho", "Ferreira", "Rodrigues", "Almeida",
            "Costa", "Gomes", "Martins", "Ribeiro", "Barbosa", "Barros", "Araújo", "Cardoso", "Correia", "Fernandes",
            "Dias", "Castro", "Nunes", "Machado", "Moreira", "Melo", "Vieira", "Freitas", "Moura", "Rocha", "Teixeira",
            "Andrade", "Azevedo", "Alves", "Duarte", "Miranda", "Cavalcante", "Campos", "Sousa", "Pinto", "Fonseca",
            "Macedo", "Mendonça", "Sales", "Torres", "Ramos", "Farias", "Monteiro", "Guimarães", "Borges", "Resende",
            "Neves", "Viana", "Santana", "Gonçalves", "Coelho", "Aguiar", "Lopes", "Amaral", "Antunes", "Camargo",
            "Bezerra", "Domingues", "Marques", "Ferraz", "Assis", "Lacerda", "Batista", "Siqueira", "Cunha", "Beltrão",
            "Campos", "Rosa", "Castilho", "Bittencourt", "Coutinho", "Chaves", "Aires", "Pacheco", "Nogueira", "Reis",
            "Simões", "Franco", "Queiroz", "Braga", "César", "Alencar", "Menezes", "Tavares", "Rangel", "Rossi", "Vieira",
            "Guerreiro", "Paes", "Xavier", "Peixoto", "Arruda", "Romero", "Magalhães", "Lira", "Toledo", "Saraiva",
            "Avelar", "Pimentel", "Cruz", "Valente", "Queirós", "Marinho", "Goulart", "Porto", "Prado", "Travassos",
            "Carmo", "França", "Brandão", "Lago", "Mota", "Campos", "Souto", "Barreto", "Faria", "Serra", "Goulart",
            "Gama", "Bueno", "Azeredo", "Maia", "Sá", "Fontes", "Alcântara", "Jardim", "Mesquita", "Fagundes", "Veiga",
            "Dantas", "Aquino", "Carneiro", "Barros", "Furtado", "Vargas", "Mansur", "Vilela", "Vasconcelos", "Sá",
            "Meireles", "Sarmento", "Sá", "Valle", "Carvalho", "Pires", "Diniz", "Lima", "Oliveira", "Rezende", "Salazar",
            "Brum", "Barros", "Gouveia", "Pessoa", "Novaes", "Mascarenhas", "Vargas", "Osório", "Serrano", "Moraes",
            "Ventura", "Amorim", "Carvalho", "Azevedo", "Barbosa", "Martins", "Rodrigues", "Cardoso", "Araújo", "Santos",
            "Cruz", "Amaral", "Ribeiro", "Gomes", "Neto", "Xavier", "Lopes", "Silveira", "Albuquerque", "Duarte", "Vieira",
            "Freire", "Macedo", "Freitas", "Campos", "Marins", "Couto", "Torrado", "Cavalcante", "Sanches", "Veloso",
            "Monteiro", "Caires", "Moura", "Furtado", "Dourado", "Pimentel", "Nogueira", "Figueira", "Araújo", "Valente",
            "Magalhães", "Brito", "Fonseca", "Garcia", "Salvador", "Santiago", "Assunção", "Matos", "Moura", "Rufino",
            "Menezes", "Nascimento", "Ramos", "Prado", "Silveira", "Queirós", "Costa", "Paiva", "Teles", "Aguiar", "Morais",
            "Castro", "Quintana", "Pereira", "Batista", "Medeiros", "Rodrigues", "Amorim", "Pinto", "Freire", "Sá", "Lemos",
            "Sanches", "Lacerda", "Valadão", "Paredes", "Fialho", "Garcia", "Pinheiro", "Serrano", "Borges", "Rezende",
            "Serra", "Costa", "Almeida", "Coimbra", "Sales", "Cavalcanti", "Teixeira", "Dias", "Melo", "Fernandes",
            "Gomes", "Nascimento", "Neves", "Azevedo", "Matos", "Garcia", "Azevedo", "Castro", "Fidalgo", "Amado",
            "Gomes", "Ramos", "Cardoso", "Fernandes", "Andrade", "Martins", "Miranda", "Reis", "Teixeira", "Vasques",
            "Moreira", "Vieira", "Ribeiro", "Cunha", "Amaral", "Queiroz", "Fonseca", "Maia", "Azevedo", "Pimentel", "Braga",
            "Meireles", "Correia", "Farias", "Santos", "Siqueira", "Monteiro", "Ribeiro", "Macedo", "Alves", "Gouveia",
            "Coelho", "Moreira", "Pena", "Leite", "Carvalho", "Lacerda", "Brito", "Fonseca", "Gonçalves", "Vasconcelos",
            "Lopes", "Castro", "Moraes", "Xavier", "Macedo", "Cabral", "Mota", "Farias", "Guimarães", "Lemos", "Paes",
            "França", "Vilela", "Barbosa", "Guerreiro", "Silva", "Coelho", "Barros", "Oliveira", "Ribeiro", "Reis", "Moraes",
            "Azevedo", "Macedo", "Couto", "Machado", "Rezende", "Pereira", "Nogueira", "Freitas", "Marques", "Sousa",
            "Sampaio", "Lopes", "Menezes", "Sampaio", "Azevedo", "Ribeiro", "Nogueira", "Monteiro", "Rocha", "Costa",
            "Gouveia", "Neto", "Santos", "Correia", "Pinto", "Monteiro", "Peixoto", "Campos", "Tavares", "Ramos", "Teixeira",
            "Paiva", "Xavier", "Nobre", "Sá", "Lira", "Machado", "Sá", "Gomes", "Nunes", "Farias", "Mendonça", "Dias", 
            "Barros", "Matos", "Assis", "Figueiredo", "Siqueira", "Marques", "Valadares", "Marins", "Serra", "Campos", 
            "Pimentel", "Dias", "Mendes", "Pereira", "Reis", "Lima", "Borges", "Aguiar", "Soares", "Amaral", "Paiva", 
            "Castilho", "Queiroz", "Guedes", "Magalhães", "Tavares", "Sanches", "Pedroso", "Lima", "Furtado", "Lobo", 
            "Reis", "Castro", "Amado", "Tavares", "Vargas", "Portela", "Santos", "Salazar", "Castro", "Oliveira", "Serrano", 
            "Neves", "Cardoso", "Moreira", "Vasques", "Dantas", "Souza", "Medeiros", "Pinto", "Araújo", "Assis", "Franco", 
            "Maia", "Guedes", "Vargas", "Silva", "Dias", "Farias", "Queiroz", "Mendonça", "Melo", "Marins", "Silva", "Sampaio", 
            "Goulart", "Rezende", "Reis", "Campos", "Couto", "Freitas", "Fonseca", "Dias", "Tavares", "Monteiro", "Sá", 
            "Marins", "Martins", "Soares", "Pinto", "Correia", "Valente", "Lima", "Pereira", "Figueiredo", "Rocha", 
            "Pimentel", "Xavier", "Campos", "Medeiros", "Ramos", "Dias", "Guedes", "Neves", "Lira", "Souza", "Peixoto", 
            "Porto", "Sampaio", "Ribeiro", "Aires", "Lima", "Franco", "Costa", "Amaral", "Moraes", "Mendes", "Almeida", 
            "Braga", "Lacerda", "Freire", "Correia", "Dias", "Monteiro", "Goulart", "Neves", "Campos", "Torrado", 
            "Serrano", "Castro", "Freitas", "Valadares", "Gomes", "Pires", "Lima"
        ]


        nome_escolhido = random.choice(lista_sobrenomes)
        nome_escolhido = unidecode(nome_escolhido)

        return nome_escolhido

    # Função para gerar nomes aleatórios
    def gerar_nomes():
        lista_nomes = [
            "Amanda Ferreira da Costa",
            "Bruno Nogueira Oliveira",
            "Camila Silva Rodrigues",
            "Diego Mendes Pereira",
            "Eduardo Vieira de Lima",
            "Fernanda Costa Souza",
            "Gabriela Alves Medeiros",
            "Henrique Cardoso Farias",
            "Igor Oliveira Gonçalves",
            "Juliana Martins Teixeira",
            "Leonardo Pereira Santos",
            "Mariana Rocha Lima",
            "Ana Beatriz Nogueira",
            "Enzo Carvalho Almeida",
            "Lidia Souza Mendes",
            "Keiller Ramos Oliveira",
            "Sofia Vieira Batista",
            "Matheus Almeida Silva",
            "Anabele Rocha Moreira",
            "Lucas Ferreira Ribeiro",
            "Paula Gonçalves Teixeira",
            "Romulo Santos Farias",
            "Daniela Costa Cardoso",
            "Felipe Silva Nogueira",
            "Raquel Mendes Oliveira",
            "Tiago Gonçalves Batista",
            "Clara Alves Pereira",
            "Vinícius Mendes de Souza",
            "Letícia Vieira Martins",
            "Marcelo Oliveira Costa",
            "Natália Ribeiro de Lima",
            "Rafael Gonçalves Azevedo",
            "Bianca Silva Santos",
            "Caio Teixeira Nogueira",
            "Larissa Costa Mendes",
            "Gustavo Alves de Souza",
            "Helena Martins Cardoso",
            "João Pedro Oliveira",
            "Camila Pereira dos Santos",
            "Miguel Costa Rodrigues",
            "Isabela Teixeira Batista",
            "Bruna Vieira Gonçalves",
            "Renan Mendes de Lima",
            "Victor Santos Cardoso",
            "Lara Silva Oliveira",
            "Fábio Mendes Almeida",
            "Tatiane Nogueira Teixeira",
            "Juliana Vieira da Costa",
            "Paulo Henrique Santos",
            "Laura Alves Pereira",
            "Marcela Rocha Gonçalves",
            "Rogério Silva Mendes",
            "Aline Nogueira de Souza",
            "Roberta Teixeira de Lima",
            "Pedro Mendes Almeida",
            "Vivian Oliveira Cardoso",
            "Andréia Costa Pereira",
            "Carlos Henrique Nogueira",
            "Bruno Teixeira Santos",
            "Marisa Vieira de Lima",
            "Luana Mendes Oliveira",
            "Ana Paula Ferreira",
            "Keila Gonçalves Mendes",
            "José Pedro Teixeira",
            "Mônica Almeida Vieira",
            "Renato Costa da Silva",
            "Fernanda Rocha Nogueira",
            "Érika Alves Batista",
            "Gabriel Silva Pereira",
            "Thiago Vieira Santos",
            "Viviane Mendes de Lima",
            "Alessandra Nogueira Teixeira",
            "Giovanna Costa Oliveira",
            "Rodolfo Vieira da Silva",
            "Patrícia Mendes Teixeira",
            "Fernando Nogueira Santos",
            "Ingrid Vieira de Lima",
            "Maurício Teixeira Gonçalves",
            "Julio Cesar Mendes",
            "Tamara Costa Oliveira",
            "Carolina Vieira da Silva",
            "Gustavo Mendes Teixeira",
            "Daniele Nogueira Santos",
            "Felipe Vieira Batista",
            "Carla Oliveira de Lima",
            "Ana Carolina Mendes",
            "Marcos Teixeira Nogueira",
            "Estela Vieira da Silva",
            "Ricardo Mendes Almeida",
            "Lia Nogueira Oliveira",
            "Adriano Vieira Teixeira",
            "Natália Mendes da Costa",
            "Fabrício Oliveira de Lima",
            "Marcia Gonçalves Silva",
            "Amanda Teixeira Vieira",
            "Rodrigo Mendes Almeida",
            "Priscila Costa da Silva",
            "Rafael Vieira Teixeira",
            "Renato Mendes de Souza",
            "Bruno Gonçalves Pereira",
            "Alice Vieira Nogueira",
            "Heitor Mendes da Costa",
            "Lívia Teixeira Santos",
            "Júlia Gonçalves Almeida",
            "Bárbara Vieira de Lima",
            "Felipe Mendes Nogueira",
            "Eliane Teixeira da Silva",
            "Tatiana Vieira Mendes",
            "Cristina Oliveira Santos",
            "Augusto Vieira de Lima",
            "Nina Mendes Teixeira",
            "Rodrigo Gonçalves da Silva",
            "Amanda Vieira Oliveira",
            "Marcelo Mendes Batista",
            "Brenda Costa Nogueira",
            "Carla Vieira de Souza",
            "Cláudio Mendes de Lima",
            "Larissa Nogueira Teixeira",
            "Milena Vieira Santos",
            "Rodrigo Teixeira Oliveira",
            "Camila Vieira Nogueira",
            "Fábio Mendes da Silva",
            "Nathalia Oliveira Teixeira",
            "Pedro Vieira Mendes",
            "Carla Teixeira da Silva",
            "Cássio Vieira Oliveira",
            "Leonardo Mendes da Costa",
            "Juliana Nogueira Teixeira",
            "Luís Fernando Vieira",
            "João Mendes Gonçalves",
            "Tatiane Oliveira Teixeira",
            "Rita Mendes da Silva",
            "Sérgio Vieira Nogueira",
            "Francisco Mendes Teixeira",
            "Mônica Vieira Oliveira",
            "Priscila Mendes da Costa",
            "Leandro Vieira Teixeira",
            "Gabriela Mendes Oliveira",
            "Sônia Teixeira Vieira",
            "Alexandre Mendes Nogueira",
            "Rosana Vieira da Silva",
            "Cristiano Teixeira Mendes",
            "Lara Vieira de Lima",
            "Fernanda Mendes Oliveira",
            "Rafael Nogueira da Silva",
            "Amanda Teixeira Mendes",
            "Roberta Vieira de Souza",
            "Vinícius Mendes da Silva",
            "Daniela Teixeira Nogueira",
            "Alex Mendes Vieira",
            "Juliano Nogueira da Costa",
            "Patrícia Vieira de Lima",
            "Luana Mendes de Souza",
            "Ricardo Teixeira Nogueira",
            "Bárbara Vieira de Souza",
            "Lucas Mendes da Costa",
            "Tatiana Nogueira Teixeira",
            "Rita Vieira de Lima",
            "Rodrigo Mendes Oliveira",
            "Cecília Nogueira da Silva",
            "Felipe Vieira de Souza",
            "Paula Mendes Teixeira",
            "Renan Vieira Oliveira",
            "Fernanda Mendes da Silva",
            "Rafaela Teixeira Nogueira",
            "Guilherme Vieira de Lima",
            "Lúcia Mendes da Costa",
            "Pedro Teixeira Nogueira",
            "Ronaldo Vieira da Silva",
            "Marcelo Mendes de Souza",
            "Júlio Mendes Vieira",
            "Amanda Vieira Nogueira",
            "Bruno Teixeira de Lima",
            "Paulo Vieira Mendes",
            "Marcela Nogueira da Silva",
            "Carolina Vieira Teixeira",
            "Marcos Mendes da Costa",
            "Lia Vieira de Lima",
            "Felipe Mendes Teixeira",
            "Rafaela Vieira da Silva",
            "Sérgio Mendes de Souza",
            "João Vieira Nogueira",
            "Aline Mendes Teixeira",
            "Lucas Vieira de Lima",
            "Roberta Mendes da Costa",
            "Daniel Teixeira de Souza",
            "Alessandra Vieira Nogueira",
            "Pedro Mendes Teixeira",
            "Fernando Vieira de Souza",
            "Letícia Mendes Oliveira",
            "Gabriel Vieira da Silva",
            "Tamara Nogueira Teixeira",
            "Ana Mendes de Souza",
            "Raquel Vieira da Silva",
            "Ricardo Mendes de Lima",
            "Cláudia Teixeira Nogueira",
            "Fábio Vieira da Silva",
            "Patrícia Mendes Nogueira",
            "Roberto Vieira de Lima",
            "Cláudio Mendes da Costa",
            "Juliana Vieira de Souza",
            "Felipe Teixeira Nogueira",
            "Luís Mendes da Silva",
            "Júlia Vieira de Lima",
            "Matheus Mendes Teixeira",
            "Paula Vieira da Silva",
            "Lara Nogueira de Souza",
            "Lucas Vieira Mendes"
        ]

        nome_escolhido = random.choice(lista_nomes)
        nome_escolhido = unidecode(nome_escolhido)

        return nome_escolhido

    # Função para selecionar as posicoes da tela do robo
    def posicao_tela(posicao):
        match posicao:
            case 1:
                return 0, 0
            case 2:
                return 400, 0
            case 3:
                return 800, 0
            case 4:
                return 1200, 0
            case 5:
                return 1600, 0
            case 6:
                return 0, 500
            case 7:
                return 400, 500
            case 8:
                return 800, 500
            case 9:
                return 1200, 500
            case 10:
                return 1600, 500
            case _:
                return None

    # Iniciar automação do site do Cassino
    def abrir_navegador(dic_navegador):
        proxy = dic_navegador["proxy"]
        usuario_planilha = dic_navegador["usuario"]
        posicao = dic_navegador["posicao_janela"]
        site = dic_navegador["site"]

        try:
            nome = gerar_nomes()
            nome_unico = nome.split(" ")
            nome_unico = nome_unico[0]

            if pd.isna(usuario_planilha) or usuario_planilha == None or len(usuario_planilha) < 4:
                if bool_checkbox_usuarioNumero_rand.get():
                    nome = gerar_nomesPrimarios()
                    sobrenome = gerar_sobrenomes()
                    usuario = nome + sobrenome
                else:
                    usuario = gerar_usuarios(nome_unico)

            else:
                usuario = usuario_planilha
        except:
            pass

        cpf = gerar_cpf()

        if bool_checkbox_senha_saque_random.get():
            senha_saque = gerar_senha_saque_random()
        else:
            senha_saque = entry_senha_saque.get()

        if bool_checkbox_senha_rand.get():
            senha = gerar_senha_random()
        else:
            senha = entry_senha_padrao.get()

        val_maximo = entry_val_max.get()
        val_minimo = entry_val_min.get()
        type_house = options_type_house.get()

        val_maximo = int(val_maximo)
        val_minimo = int(val_minimo)

        try:
            valor = random.randint(val_minimo, val_maximo)
        except:
            valor = random.randint(val_maximo, val_minimo)

        if posicao >= 11:
            posicao -= 10

        x, y = posicao_tela(posicao=posicao)

        if type_house == "Casa 2" or type_house == "Casa 3":
            larg = 400
            alt = 1000
        else:
            larg = 400
            alt = 500

        myproxy = proxy

        qtd = verificar_pontos(myproxy)

        if int(qtd) == 3:
            dados_proxy = myproxy.split(":")
            proxy_host = dados_proxy[0]
            proxy_port = dados_proxy[1]
            proxy_username = dados_proxy[2]
            proxy_password = dados_proxy[3]
        else:
            dados_proxy = myproxy.split(":")
            proxy_host = dados_proxy[0]
            proxy_port = dados_proxy[1]

        chave_pix = "Nenhum"
        chrome = "Nenhum"
        idioma = "Pt-Br"
        url_atual = dic_navegador["site"]

        nome_unico = unidecode(nome_unico)
        nome = unidecode(nome)

        dados_navegador = {
            "posicao_janela": posicao,
            "usuario": usuario,
            "senha": senha,
            "nome": nome,
            "nome_unico": nome_unico,
            "driver": chrome,
            "site": url_atual,
            "proxy": proxy,
            "idioma": idioma,
            "valor": valor,
            "cpf": cpf,
            "senha_saque": senha_saque,
            "chave_pix": chave_pix
        }

        # Inicializando as configurações do Chrome
        if proxy_password and proxy_username:
            proxy_host, proxy_port, proxy_user, proxy_pass = formatar_proxy(proxy)

            chrome = create_chromedriver(proxy_host, proxy_port, proxy_user, proxy_pass, x, y, alt, larg, posicao, dados_navegador)

        else:
            chrome_options = Options()
            arguments = ['--incognito', '--disable-cache', '--lang=pt-BR', '--disable-notifications', '--disable-popup-blocking',
                         '--disable-geolocation', f'--proxy-server=http://{proxy_host}:{proxy_port}', f"--window-position={x},{y}", f"--window-size={alt},{larg}"]

            for argument in arguments:
                chrome_options.add_argument(argument)

            chrome = webdriver.Chrome(options=chrome_options)

        novo_driver = {"driver": chrome}
        dados_navegador.update(novo_driver)

        wait = WebDriverWait(chrome, 10)  # Espera por até 10 segundos

        chrome.get(site)

        idioma = "Pt"
        while len(chrome.find_elements(By.XPATH, "//input[@type='text']")) < 1:
            sleep(1)
            if len(chrome.find_elements(By.XPATH, "//input[@placeholder='Member account']")) == 1:
                idioma = "Ingles"
                sleep(0.5)
            if idioma == "Ingles":
                return message_erro(f"Navegador {posicao} está em inglês, mude o idioma do seu windows!")

            if len(chrome.find_elements(By.XPATH, "//input[@type='password']")) >= 1:
                try:
                    chrome.find_elements(By.XPATH, "//input[@type='password']")
                    break
                except:
                    pass

        try:
            # Armazenar o identificador da guia original
            url_atual = chrome.current_url

            # Preenchendo os campos de usuário
            campos_usuario = [
                "//input[@type='text' and @maxlength='16' and @autocomplete='off']",
                "//input[@placeholder='Por favor, insira Conta ']",
                "//input[@placeholder='Por favor, insira Conta / Número do Celular ']",
                "//input[contains(@placeholder, 'Digite o Conta')]",
                "//input[@placeholder='Nome de usuário']",
                "//input[@placeholder='Nome de Usuário']",
                "//input[@class='ant-select-search__field']"
            ]
            for xpath in campos_usuario:
                try:
                    chrome.find_element(By.XPATH, xpath).send_keys(usuario)
                    break
                except:
                    continue

            # Preenchendo a senha
            campos_senha = [
                "//input[@placeholder='Senha']",
                "//input[@type='password' and @maxlength='16' and @autocomplete='new-password']"
            ]
            for xpath in campos_senha:
                try:
                    chrome.find_element(By.XPATH, xpath).send_keys(senha)
                    break
                except:
                    continue

            # Preenchendo a confirmação da senha
            campos_senha_confirm = [
                "//input[@placeholder='Confirme a senha novamente, o mesmo que a senha!']",
                "//input[@placeholder='Por favor, confirme sua senha novamente']",
                "//input[@placeholder='Confirme senha']",
                "//input[@placeholder='Confirme a senha']",
                "//input[@type='text' and @autocomplete='new-password']"
            ]
            for xpath in campos_senha_confirm:
                try:
                    chrome.find_element(By.XPATH, xpath).send_keys(senha)
                    break
                except:
                    continue

            # Campo do nome verdadeiro
            try:
                chrome.find_element(
                    By.XPATH, "//input[@placeholder='Preencha o nome verdadeiro e torne -o conveniente para a retirada posterior!']").send_keys(nome_unico)
            except:
                try:
                    chrome.find_element(
                        By.XPATH, "//input[@placeholder='Nome completo']").send_keys(nome)
                except:
                    pass

            try:
                telefone = gerar_numero_telefone()
                chrome.find_element(By.XPATH, "//input[@placeholder='Digite o Número do Celular']").send_keys(telefone)
            except:
                pass

            if type_house == "Casa 2" or type_house == "Casa 3":
                sleep(2)

            data = datetime.now()

            # Clicando no botão de registrar
            botoes_registrar = [
                "//button[@class='ant-btn ant-btn-primary ant-btn-block GaL3XJonIwzK4ZeJyCyq']",
                "//div[@class='now-btn']",
                "//button[contains(@class, 'van-button--default')]",
                "//div[@class='registerSuccess-btn-QPIyr']",
                "//button[contains(@class, 'button _submitButton_34mo6_15')]",
                "//button[contains(@class, '_submitButton_t1v6q_63')]",
                "//button[contains(@class, 'ant-btn ant-btn-primary ant-btn-block')]",
                "//button[@class='ant-btn ant-btn-primary ant-btn-block UfYvdDE9GdeKbnBtnMjg']",
                "//button[@class='ant-btn ant-btn-primary ant-btn-block BvvAH2jDNsmGodhqACCz']"
            ]
            for xpath in botoes_registrar:
                try:
                    chrome.find_element(By.XPATH, xpath).click()
                    break
                except:
                    continue

            contador = 0

            if "Casa 1" in type_house:
                saida = False

                while len(chrome.find_elements(By.XPATH, "//button[contains(@class, 'BvvAH2jDNsmGodhqACCz')]")) < 1:
                    sleep(1)
                try:
                    chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'BvvAH2jDNsmGodhqACCz')]").click()
                    saida = True
                except:
                    try:
                        resposta = chrome.find_element(
                            By.XPATH, "//span[@class='azs6RKGF2DadE09dhZqO']").text
                        if resposta.startswith("Download"):
                            chrome.find_element(
                                By.XPATH, "(//div[@class='closeIcon'])[1]").click()
                        elif "download" in resposta or "bonus" in resposta or "Descarregue" in resposta or "App" in resposta:
                            chrome.find_element(
                                By.XPATH, "(//div[@class='closeIcon'])[1]").click()
                    except:
                        pass

            elif "Casa 2" in type_house:
                while len(chrome.find_elements(By.XPATH, "//div[@class='ant-modal-content']")) < 1:
                    sleep(1)
                    try:
                        chrome.find_element(
                            By.XPATH, "//div[contains(@class, 'registerSuccess-btn-QPIyr')]").click()
                        break
                    except:
                        pass
                    try:
                        chrome.find_element(
                            By.XPATH, "//button[contains(@class, 'BvvAH2jDNsmGodhqACCz')]").click()
                        break
                    except:
                        pass
                    contador += 1
                    if contador == 250:
                        break

                while len(chrome.find_elements(By.XPATH, "//input[@class='ant-input' and @type='tel']")) < 1:
                    sleep(1)
                    contador += 1
                    if contador == 8:
                        break
            elif "Casa 3" in type_house:
                while len(chrome.find_elements(By.XPATH, "//div[@role='alert']")) < 1:
                    sleep(1)

            else:
                while len(chrome.find_elements(By.XPATH, "//input[@class='ant-input' and @type='text']")) < 1:
                    sleep(1)
                    contador += 1
                    if contador == 8:
                        break

            sleep(3)

            # Inserindo o valor.
            try:

                try:
                    # Localizar o checkbox e clicar nele
                    checkbox_element = chrome.find_element(
                        By.XPATH, '//input[@type="checkbox" and contains(@class, "ant-checkbox-input")]')
                    if not checkbox_element.is_selected():
                        checkbox_element.click()

                    # Localizar o botão de fechar e clicar nele
                    chrome.find_element(
                        By.XPATH, '//span[contains(@class, "cms-close-btn-Xqx5l") and contains(@class, "cms-close-btn-round-fI4sS")]').click()
                except:
                    pass

                try:
                    sleep(1)
                    chrome.find_element(
                        By.XPATH, "//div[@class='downloadPopup-close-rgQal']").click()
                except:
                    pass

                try:
                    chrome.find_element(
                        By.XPATH, "//input[contains(@placeholder, 'Mínimo') and contains(@placeholder, 'Máximo')]").send_keys(valor)
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//input[@placeholder='Mínimo 10, Máximo 50000']").send_keys(valor)
                    except:
                        try:
                            chrome.find_element(
                                By.XPATH, "//input[contains(@placeholder, 'Minimo') and contains(@placeholder, 'Maximo')]").send_keys(valor)
                        except:
                            pass
                try:
                    chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'ant-btn') and contains(@class, 'ant-btn-primary')]").click()
                except:
                    chrome.find_element(
                        By.XPATH, "//button[@class='ant-btn ant-btn-primary Z3d3LY3KzBEXr0Mc4b_l']").click()
            except:
                pass

        except Exception as e:

            print(f"Erro: {e}")

        if "gml777" in url_atual:
            abas.append((chrome, url_atual, idioma))
            chrome.execute_script("window.scrollBy(0, 90);")
        else:
            # Armazena todos os identificadores de guias abertas
            guias = chrome.window_handles

            # Supondo que a nova guia seja a última aberta, você pode mudar para ela usando:
            nova_guia = guias[-1]
            chrome.switch_to.window(nova_guia)

            with open('Usuarios.txt', 'a') as arquivo:
                # Cria a linha a ser adicionada
                linha = f"{usuario} - {senha_saque} - {senha} - {proxy} - {nome_unico} - {site} - {data} - {cpf} - \n"
                # Escreve a linha no arquivo
                arquivo.write(linha)

            abas.append(dados_navegador)
            sleep(3)
            chrome.execute_script("window.scrollBy(0, 150);")

        while True:
            sleep(25)

    def jogar(dados_navegador):
        chrome = dados_navegador["driver"]
        url = dados_navegador["site"]

        type_house = options_type_house.get()

        if type_house == "Casa 2":
            try:
                game = dropbox_games.get()
                nova_url = modificar_url(
                    url, novo_caminho="/game/gameSubList/EGAME/PP/PPLATAM_EGAME/PPLATAM/7954468286452", nova_query="nenhum")

                chrome.get(nova_url)

                while len(chrome.find_elements(By.XPATH, "//input[@placeholder='Pesquisar' and @type='text']")) < 1:
                    sleep(1)

                campo_pesquisar_game = chrome.find_element(
                    By.XPATH, "//input[@placeholder='Pesquisar' and @type='text']")
                fechar_avisos(chrome)
                campo_pesquisar_game.send_keys(game)

                campo_pesquisar_game.send_keys(Keys.ENTER)
                sleep(0.5)
            except:
                pass
        elif type_house == "Casa 1":
            try:
                game = dropbox_games.get()
                if "gml777" in url:
                    nova_url = modificar_url(
                        url, novo_caminho="/#/subgame", nova_query="nenhum")

                    chrome.get(nova_url)

                    while len(chrome.find_elements(By.XPATH, "//input[@class='input-keyword' and @type='text']")) < 1:
                        sleep(1)

                    campo_pesquisar_game = chrome.find_element(
                        By.XPATH, "//input[@class='input-keyword' and @type='text']")
                    fechar_avisos(chrome)
                    campo_pesquisar_game.send_keys(game)

                    campo_pesquisar_game.send_keys(Keys.ENTER)
                    sleep(0.5)

                    try:
                        chrome.find_element(
                            By.XPATH, "(//div[contains(@class, 'advertisement-box')])[1]").click()
                    except:
                        chrome.find_element(
                            By.XPATH, "//div[@class='subgame-item']").click()
                elif "panterapg" in url:
                    try:
                        chrome.get()
                        chrome.get(nova_url)
                        sleep(1)
                    except:
                        pass
                    try:
                        chrome.find_element(
                            By.XPATH, "//div[@id='label_Slots']").click()
                        sleep(1)
                    except:
                        pass
                    try:
                        chrome.find_element(
                            By.XPATH, "//input[@placeholder='Procurar jogos']").send_keys(game)
                        campo_pesquisar_game.send_keys(Keys.ENTER)
                        sleep(0.5)
                        chrome.find_element(
                            By.CLASS_NAME, "_game_list_item_1oyfd_3 button").click()
                    except:
                        pass
                else:
                    nova_url = modificar_url(
                        url, novo_caminho="/home/search", nova_query="nenhum")

                    chrome.get(nova_url)

                    while len(chrome.find_elements(By.XPATH, "//input[@class='ant-input' and @type='text']")) < 1:
                        sleep(1)

                    campo_pesquisar_game = chrome.find_element(
                        By.XPATH, "//input[@class='ant-input' and @type='text']")
                    fechar_avisos(chrome)
                    campo_pesquisar_game.send_keys(game)

                    campo_pesquisar_game.send_keys(Keys.ENTER)
                    sleep(0.5)
                    chrome.find_element(
                        By.XPATH, "//div[@data-status='loaded' and @role='OuterBox']").click()

                    try:
                        fechar_avisos(chrome)
                        sleep(0.5)
                        try:
                            try:
                                screen_game = chrome.find_element(
                                    By.XPATH, "//div[@class='uQNZtvR6K74JV8XnzP22']")
                                screen_game.find_element(
                                    By.XPATH, "//div[@data-status='loaded']").click()
                            except:
                                try:
                                    jogo = chrome.find_elements(
                                        By.XPATH, "//div[contains(@class, 'advertisement-box')]")
                                    jogo[0].click()
                                except:
                                    try:
                                        chrome.find_element(
                                            By.XPATH, "//div[@class='subgame-item']").click()
                                    except:
                                        chrome.find_element(
                                            By.XPATH, "//div[@data-status='loaded' and @role='OuterBox']").click()

                        except:
                            try:
                                game_escolhido = chrome.find_elements(
                                    By.XPATH, "//div[@data-status='loaded' and @role='OuterBox']")
                                game = game.lower()
                                if game == "hot to burn" and "bjb777" in url:
                                    game_escolhido[0].click()
                                elif game == "hot to burn":
                                    game_escolhido[1].click()
                                else:
                                    game_escolhido[0].click()
                            except:
                                pass
                    except:
                        pass
            except:
                pass

        try:
            chrome.find_element(By.XPATH, "//input[@type='checkbox']").click()
        except:
            pass

        try:
            resposta = chrome.find_element(
                By.XPATH, "//span[@class='azs6RKGF2DadE09dhZqO']").text
            if resposta.startswith("Download"):
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()
            elif "download" in resposta or "bonus" in resposta or "Descarregue" in resposta:
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()

        except:
            pass

        while True:
            sleep(15)

    def cadastrar_pix(dados_navegador):
        cpf = dados_navegador["cpf"]
        chrome = dados_navegador["driver"]
        link = dados_navegador["site"]
        nome = dados_navegador["nome_unico"]

        senha_criada = False
        if bool_checkbox_senha_saque_random.get():
            senha_saque = dados_navegador["senha_saque"]
        else:
            senha_saque = entry_senha_saque.get()
        modelo_chave_pix = dropbox_modelo_pix.get()
        type_house = options_type_house.get()

        if type_house == "Casa 2":
            # Link para alterar a senha/criar senha
            url_criar_senha = modificar_url(
                link, novo_caminho="/withdrawPassword", nova_query="nenhum")
            chrome.get(url_criar_senha)

            while len(chrome.find_elements(By.XPATH, "//input[@class='withdrawPasswordInput-jxyTr']")) < 1:
                sleep(1)
        else:
            # Link para alterar a senha/criar senha
            url_criar_senha = modificar_url(
                link, novo_caminho="/home/security", nova_query="current=5&isCallbackWithdraw=0")
            chrome.get(url_criar_senha)

            while len(chrome.find_elements(By.XPATH, "//input[@class='k54PxY4rjAorQBZf12Ab']")) < 1:
                sleep(1)

        try:
            tela_alterar_senha = chrome.find_element(
                By.XPATH, "//span[contains(text(), 'Reset Withdraw Password')]")
            senha_criada = True
        except:
            try:
                tela_alterar_senha = chrome.find_element(
                    By.XPATH, "//span[contains(text(), 'Alterar Senha')]")
                senha_criada = True
            except:
                pass

        fechar_avisos(chrome)

        if senha_criada == False:
            if type_house == "Casa 2":
                try:
                    campos = chrome.find_elements(
                        By.XPATH, "//input[@class='withdrawPasswordInput-jxyTr']")

                    campos[0].send_keys(senha_saque)
                    fechar_avisos(chrome)
                    campos[1].send_keys(senha_saque)
                    fechar_avisos(chrome)
                except:
                    pass
                try:
                    btn_confirmar = chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'van-button--default')]")
                    btn_confirmar.click()
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//button[@type='button']").click()
                    except:
                        pass

            else:
                try:
                    campos = chrome.find_elements(
                        By.XPATH, "//input[@type='number' and @maxlength='6']")

                    campos[0].send_keys(senha_saque)
                    fechar_avisos(chrome)
                    campos[1].send_keys(senha_saque)
                    fechar_avisos(chrome)
                except:
                    pass
                try:
                    btn_confirmar = chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'verification-btn__next')]")
                    btn_confirmar.click()
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//button[@type='button']").click()
                    except:
                        pass

            sleep(2)
            # while len(chrome.find_elements(By.XPATH, "//div[contains(text(), 'Palavra-passe')]")) < 1:
            #    sleep(0.1)

        if type_house == "Casa 2":
            # Link para alterar a senha/criar senha
            url_criar_senha = modificar_url(
                link, novo_caminho="/withdraw", nova_query="current=3")
            chrome.get(url_criar_senha)

            while len(chrome.find_elements(By.XPATH, "//div[@class='manage-account-yvrTf']")) < 1:
                sleep(1)

        else:
            url_criar_chave = modificar_url(
                link, novo_caminho="/home/withdraw", nova_query="current=3")
            chrome.get(url_criar_chave)

            while len(chrome.find_elements(By.CLASS_NAME, "iF8_fapSvlOlgo6gKh8B")) < 1:
                sleep(1)

        try:
            if type_house == "Casa 2":

                try:
                    chrome.find_element(
                        By.XPATH, "//div[@class='manage-account-yvrTf']").click()
                except:
                    try:
                        chrome.find_element(
                            By.CLASS_NAME, "_accountContainer_1af74_598").click()
                    except:
                        pass

                while len(chrome.find_elements(By.XPATH, "//input[@class='withdrawPasswordInput-_uEFJ' and @maxlength='6']")) < 1:
                    sleep(1)

                campo_senha = chrome.find_element(
                    By.XPATH, "//input[@class='withdrawPasswordInput-_uEFJ' and @maxlength='6']")
                campo_senha.send_keys(senha_saque)
                try:
                    chrome.find_element(
                        By.XPATH, "//button[@class='ant-btn ant-btn-primary ant-btn-lg']").click()
                except:
                    pass
            # Botão para Add Pix
            else:
                try:
                    chrome.find_element(
                        By.CLASS_NAME, "VRELRka6V8vK1gNMRtTQ").click()
                except:
                    try:
                        chrome.find_element(
                            By.CLASS_NAME, "_accountContainer_1af74_598").click()
                    except:
                        pass

                while len(chrome.find_elements(By.XPATH, "//input[@type='number' and @maxlength='6']")) < 1:
                    sleep(1)

                campo_senha = chrome.find_element(
                    By.XPATH, "//input[@type='number' and @maxlength='6']")
                campo_senha.send_keys(senha_saque)
                try:
                    chrome.find_element(
                        By.XPATH, "//button[@class='ant-btn ant-btn-primary JHBAn8W0jkHI1OM_X2fy']").click()
                except:
                    pass

            while len(chrome.find_elements(By.XPATH, "//div[contains(@class, 'ant-modal-title') and contains(text(), 'PIX')]")) < 1:
                try:
                    chrome.find_element(
                        By.XPATH, "//p[contains(@class, '_title_12i5b_72') and contains(text(), 'PIX')]")
                    break
                except:
                    sleep(1)

            try:
                campo_nome = chrome.find_element(
                    By.XPATH, "//input[@placeholder='Insira o nome']")
            except:
                try:
                    campo_nome = chrome.find_element(
                        By.XPATH, "//input[@placeholder='Digite seu nome verdadeiro']")
                except:
                    pass

            try:
                campo_cpf = chrome.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'CPF')]")
                try:
                    dropdown = chrome.find_element(
                        By.XPATH, "//div[@class='ant-select ant-select-enabled']")
                except:
                    dropdown = chrome.find_element(
                        By.XPATH, "//div[@class='ant-select-selector']")

                if modelo_chave_pix == "Email":

                    dropdown.click()
                    option_cpf = dropdown.find_element(
                        By.XPATH, "//li[@role='option' and @name='EMAIL']")
                    option_cpf.click()
                    sleep(1)

                elif modelo_chave_pix == "Telefone":
                    dropdown.click()
                    option_cpf = dropdown.find_element(
                        By.XPATH, "//li[@role='option' and @name='PHONE']")
                    option_cpf.click()
                    sleep(1)

                elif modelo_chave_pix == "Cpf":
                    dropdown.click()
                    option_cpf = dropdown.find_element(
                        By.XPATH, "//li[@role='option' and @name='CPF']")
                    option_cpf.click()
                elif modelo_chave_pix == "Chave aleatória":
                    dropdown.click()
                    option_cpf = dropdown.find_element(
                        By.XPATH, "//li[@role='option' and @name='EVP']")
                    option_cpf.click()
            except:
                pass

            # if chave_pix:
            #     campo_chave_pix = chrome.find_element(By.XPATH, "//input[@placeholder='Introduza a sua conta PIX']")
            #     campo_chave_pix.send_keys(chave_pix)

            if "bjb777" in link or "aza777" in link:
                pass
            else:
                try:
                    campo_nome.send_keys(nome)
                except:
                    pass
            sleep(0.5)
            try:
                campo_cpf = chrome.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'cpf')]")
            except:
                campo_cpf = chrome.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'CPF')]")

            campo_cpf.send_keys(cpf)

            try:
                campo_nome = chrome.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'nome')]")
            except:
                campo_nome = chrome.find_element(
                    By.XPATH, "//input[contains(@placeholder, 'Nome')]")

            try:
                campo_nome.send_keys(nome)
            except:
                nome = gerar_nomes()
                campo_nome.send_keys(nome)

        except Exception as e:
            print(e)
            pass

        sleep(3)

        try:
            chrome.find_element(By.XPATH, "//input[@type='checkbox']").click()
        except:
            pass

        try:
            resposta = chrome.find_element(
                By.XPATH, "//span[@class='azs6RKGF2DadE09dhZqO']").text
            if resposta.startswith("Download"):
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()
            elif "download" in resposta or "bonus" in resposta or "Descarregue" in resposta:
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()

        except:
            pass

        while True:
            sleep(15)

    def inserir_chave(dados_navegador):
        chrome = dados_navegador["driver"]
        chave = dados_navegador["chave"]

        try:
            chrome.find_element(
                By.XPATH, "//input[contains(@placeholder, 'PIX') or contains(@placeholder, 'pix')]").send_keys(chave)
            chrome.find_element(
                By.XPATH, "//button[contains(@class, 'uIzYvPhfmLQ5pMto7Omn')]").click()
        except:
            pass

    def depositar(dados_navegador):
        chrome = dados_navegador["driver"]
        site = dados_navegador["site"]

        val_maximo = entry_val_max.get()
        val_minimo = entry_val_min.get()
        chrome.get(site)

        try:
            while chrome.find_elements(By.XPATH, "//main[@class='ant-layout-content']") < 1:
                sleep(1)

            itens = chrome.find_elements(
                By.CLASS_NAME, "fzTE3kPaq_bjTxdoKUUY PIj1PfbzHvacLB3SeEjQ")
            itens[2].click()
            while len(chrome.find_elements(By.XPATH, "//input[@class='ant-input' and @type='text']")) < 1:
                sleep(1)
                contador += 1
                if contador == 8:
                    break

            fechar_avisos(chrome)

            campo_valor_recarga = chrome.find_element(
                By.XPATH, "//input[contains(@placeholder, 'Mínimo') and contains(@placeholder, 'Máximo')]")

            valor = random.randint(val_minimo, val_maximo)
            campo_valor_recarga.send_keys(valor)
            btn_recarregar = chrome.find_element(
                By.XPATH, "//button[@class='ant-btn ant-btn-primary Z3d3LY3KzBEXr0Mc4b_l']")
            btn_recarregar.click()
        except:
            pass

        while True:
            sleep(15)

    def sacar_completo(dados_navegador):
        chrome = dados_navegador["driver"]
        link = dados_navegador["site"]

        type_house = options_type_house.get()
        try:
            if type_house == "Casa 2":
                if bool_checkbox_senha_saque_random.get():
                    senha_saque = dados_navegador["senha_saque"]
                else:
                    senha_saque = entry_senha_saque.get()
                nova_url = modificar_url(
                    link, novo_caminho="/withdraw", nova_query="current=0")

                chrome.get(nova_url)
                contador = 0

                while len(chrome.find_elements(By.XPATH, "//div[@class='withdraw-xCDi0']")) < 1:
                    sleep(1)
                    contador += 1
                    if contador == 10:
                        break

                sleep(2)

                try:
                    chrome.find_element(
                        By.XPATH, "//span[contains(@class, 'ant-input-suffix')]").click()
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//span[@class='withdraw-input-suffix-n4MoZ']").send_keys(senha_saque)
                    except:
                        pass

                try:
                    chrome.find_element(
                        By.XPATH, "//input[@type='number']").send_keys(senha_saque)
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//input[@maxlength='6']").send_keys(senha_saque)
                    except:
                        pass
                sleep(1)
                try:
                    chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'whKvP0fKErR_J8VBaFio') and contains(@class, 'ant-btn ant-btn-primary')]").click()
                except:
                    pass

            else:
                senha_saque = entry_senha_saque.get()
                nova_url = modificar_url(
                    link, novo_caminho="/home/withdraw", nova_query="current=0")

                chrome.get(nova_url)

                while len(chrome.find_elements(By.XPATH, "//input[@type='number']")) < 1:
                    sleep(1)

                try:
                    chrome.find_element(
                        By.XPATH, "//span[contains(@class, 'ant-input-suffix')]").click()
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//span[@class='withdraw-input-suffix-n4MoZ']").send_keys(senha_saque)
                    except:
                        pass

                try:
                    chrome.find_element(
                        By.XPATH, "//input[@type='number']").send_keys(senha_saque)
                except:
                    try:
                        chrome.find_element(
                            By.XPATH, "//input[@maxlength='6']").send_keys(senha_saque)
                    except:
                        pass

                sleep(1)
                try:
                    chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'whKvP0fKErR_J8VBaFio') and contains(@class, 'ant-btn ant-btn-primary')]").click()
                except:
                    pass
        except:
            pass

        sleep(2.5)
        try:
            resposta = chrome.find_element(
                By.XPATH, "//span[@class='azs6RKGF2DadE09dhZqO']").text
            if resposta.startswith("Download"):
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()
            elif "download" in resposta or "bonus" in resposta or "Descarregue" in resposta:
                chrome.find_element(
                    By.XPATH, "(//div[@class='closeIcon'])[1]").click()

        except:
            pass

        while True:
            sleep(15)

    def coletar_bonus(dados_navegador):
        chrome = dados_navegador["driver"]
        link = dados_navegador["site"]
        type_house = options_type_house.get()
        try:
            if type_house == "Casa 2":
                nova_url = modificar_url(
                    link, novo_caminho="/activity", nova_query="tab=4")
                chrome.get(nova_url)

                while len(chrome.find_elements(By.XPATH, "//div[@class='name']")) < 1:
                    sleep(1)

                try:
                    chrome.find_elements(
                        By.XPATH, "//div[@class, 'btn')]")[1].click()
                except:
                    pass
                try:
                    chrome.find_elements(
                        By.XPATH, "//div[@class, 'btn')]")[0].click()
                except:
                    pass

            else:
                nova_url = modificar_url(
                    link, novo_caminho="/home/event/item/10/8", nova_query="nenhum")
                chrome.get(nova_url)

                while len(chrome.find_elements(By.XPATH, "//span[@class='ant-table-column-title']")) < 1:
                    sleep(1)

                try:
                    chrome.find_element(
                        By.XPATH, "//button[contains(@class, 'ant-btn-success')]").click()
                except:
                    pass
        except:
            pass
        while True:
            sleep(20)

    def fechar_abas():
        try:
            for chrome in abas:
                chrome.quit()
            abas.clear()
        except:
            pass

    def ativar_inserir_chave():
        chaves = []

        # Abre o arquivo "Chaves Pix.txt" no modo de leitura
        with open("Chaves Pix.txt", "r", encoding="utf-8") as arquivo:
            # Lê todas as linhas do arquivo e armazena na lista 'chaves'
            chaves = arquivo.readlines()

        # Remove os caracteres de nova linha (\n) das extremidades das linhas
        chaves = [linha.strip() for linha in chaves]

        abas = verificar_e_remover_abas_fechadas()

        for (chrome, link, idioma), chave in zip(abas, chaves):
            inserir_chave(chrome, link, chave=chave)

    def ativar_depositar():
        for dados_navegador in abas:
            iniciar_inserir_chave(dados_navegador)

    def ativar_jogar():
        for dados_navegador in abas:
            iniciar_jogar(dados_navegador)
            ultimo_url = dados_navegador["site"]
        mac = obter_endereco_mac()
        try:
            jogo_atual = dropbox_games.get()
            qtd_telas = options_qtd_loop.get()

            url_desc_game = "https://script.google.com/macros/s/AKfycbxUST8kEp1xVakdqBK0CxtfCYc-sCEX665mKRwXpqBUvR0fO8Ig_PMnB0JSomJLhYomGg/exec"

            horario = datetime.now().isoformat()

            dados = {
                'mac_address': mac,
                'site': ultimo_url,
                'jogo': jogo_atual,
                'horario': horario,
                'telas': qtd_telas
            }

            requests.post(url=url_desc_game, json=dados)
        except:
            pass

    def ativar_coletar_bonus():
        for dados_navegador in abas:
            iniciar_coletar_bonus(dados_navegador)

    def ativar_sacar_completo():
        for dados_navegador in abas:
            iniciar_sacar_completo(dados_navegador)

    def ativar_cadastrar_pix():
        for dados_navegador in abas:
            iniciar_cadastrar_pix(dados_navegador)

    def add_game():
        item = dropbox_games.get()
        if item != "" and item != " " and item not in list(list_games):
            list_games.append(item)
        senha_saque, senha_padrao, val_max, val_min, site,qdt_loop,modelo_pix,type_house = consultar_txt()

        conteudo =f"jogos={list_games};valor_max={val_max};valor_min={val_min};senha_saque={senha_saque};senha_padrao={senha_padrao};site={site};qdt_loop={qtd_loop};type_house={type_house};modelo_pix={modelo_pix};usuarioNumero_rand={usuarioNumero_rand};senha_saque_random={senha_saque_random};senha_rand={senha_rand};tempoCriacao_rand={tempoCriacao_rand};mobile={mobile};ecoproxy={ecoproxy}"

        with open(caminho_cfg, 'w') as arquivo:
            arquivo.write(conteudo)
        message_success("Jogo adicionado com Sucesso!")

    def remove_game():
        item = dropbox_games.get()
        if item != "" and item != " " and item in list(list_games):
            list_games.remove(item)

        senha_saque, senha_padrao, val_max, val_min, site,qdt_loop,modelo_pix,type_house  = consultar_txt()

        conteudo =f"jogos={list_games};valor_max={val_max};valor_min={val_min};senha_saque={senha_saque};senha_padrao={senha_padrao};site={site};qdt_loop={qtd_loop};type_house={type_house};modelo_pix={modelo_pix};usuarioNumero_rand={usuarioNumero_rand};senha_saque_random={senha_saque_random};senha_rand={senha_rand};tempoCriacao_rand={tempoCriacao_rand};mobile={mobile};ecoproxy={ecoproxy}"


        with open(caminho_cfg, 'w') as arquivo:
            arquivo.write(conteudo)
        item = dropbox_games.get()
        if item != "" and item != " " and item in list(list_games):
            list_games.remove(item)

        senha_saque, senha_padrao, val_max, val_min, site,modelo_pix,type_house = consultar_txt()

        conteudo = f"jogos={list_games};valor_max={val_max};valor_min={val_min};senha_saque={senha_saque};senha_padrao={senha_padrao};site={site}"

        with open(caminho_cfg, 'w') as arquivo:
            arquivo.write(conteudo)

        message_success("Jogo removido com Sucesso!")

    def iniciar_depositar(dados_navegador):
        threading.Thread(target=depositar, args=(dados_navegador,)).start()

    def iniciar_inserir_chave(dados_navegador):
        threading.Thread(target=inserir_chave, args=(dados_navegador,)).start()

    def iniciar_jogar(dados_navegador):
        threading.Thread(target=jogar, args=(dados_navegador,)).start()

    def iniciar_coletar_bonus(dados_navegador):
        threading.Thread(target=coletar_bonus, args=(dados_navegador,)).start()

    def iniciar_sacar_completo(dados_navegador):
        threading.Thread(target=sacar_completo,
                         args=(dados_navegador,)).start()

    def iniciar_cadastrar_pix(dados_navegador):
        threading.Thread(target=cadastrar_pix, args=(dados_navegador,)).start()

    # Ativar ações multithread
    def iniciar_abrir_navegador(dicionario_navegador):
        thread = threading.Thread(
            target=abrir_navegador, args=(dicionario_navegador,))
        thread.start()  # Inicia a thread
        threads.append(thread)

    # Atualizar informacoes salvas.
    def atualizar_infos():
        senha_saque_dig = entry_senha_saque.get()
        senha_padrao_dig = entry_senha_padrao.get()
        game = dropbox_games.get()
        val_min_dig = entry_val_min.get()
        val_max_dig = entry_val_max.get()
        site_dig = entry_site.get()
        qtd_loop =  options_qtd_loop.get()
        type_house_dig = options_type_house.get()
        modelo_pix_dig = dropbox_modelo_pix.get()
        bool_mobile = bool_checkbox_mobile.get()
        mobile = str(bool_mobile)
        senha_saque, senha_padrao, val_max, val_min, site,qdt_loop,modelo_pix,type_house  = consultar_txt()
        if val_max_dig != "":
            val_max = val_max_dig
        if val_min_dig != "":
            val_min = val_min_dig
        if senha_padrao_dig != "":
            senha_padrao = senha_padrao_dig
        if senha_saque_dig != "":
            senha_saque = senha_saque_dig
        if site_dig != "":
            site = site_dig
        if game != "" and game != " " and len(game) > 4 and game != "," and "":
            list_games.append(game)

        if modelo_pix_dig != "":
            modelo_pix = modelo_pix_dig
        if type_house_dig != "":
            type_house = type_house_dig
            
        usuarioNumero_rand = bool_checkbox_usuarioNumero_rand.get()
        senha_saque_random = bool_checkbox_senha_saque_random.get()
        senha_rand = bool_checkbox_senha_rand.get()
        tempoCriacao_rand = bool_checkbox_tempoCriacao_rand.get()
        bool_mobile = bool_checkbox_mobile.get()
        ecoproxy = bool_checkbox_ecoproxy.get()
        
        
        conteudo = f"jogos={list_games};valor_max={val_max};valor_min={val_min};senha_saque={senha_saque};senha_padrao={senha_padrao};site={site};qdt_loop={qtd_loop};type_house={type_house};modelo_pix={modelo_pix};usuarioNumero_rand={usuarioNumero_rand};senha_saque_random={senha_saque_random};senha_rand={senha_rand};tempoCriacao_rand={tempoCriacao_rand};mobile={mobile};ecoproxy={ecoproxy}"


        with open(caminho_cfg, 'w') as arquivo:
            arquivo.write(conteudo)

        message_success("Informações foram atualizadas!")


    # Iniciando os campos e opções da interface
    if vartxt_val_max != None and vartxt_val_max != "" and vartxt_val_max != " ":
        entry_val_max = ctk.CTkEntry(ajustes_frame, textvariable=vartxt_val_max,
                                     placeholder_text="Digite o valor máximo...", width=250, height=35)
    else:
        entry_val_max = ctk.CTkEntry(
            ajustes_frame, placeholder_text="Digite o valor máximo...", width=250, height=35)

    if vartxt_val_min != None and vartxt_val_max != "":
        entry_val_min = ctk.CTkEntry(ajustes_frame, textvariable=vartxt_val_min,
                                     placeholder_text="Digite o valor mínimo...", width=250, height=35)
    else:
        entry_val_min = ctk.CTkEntry(
            ajustes_frame, placeholder_text="Digite o valor mínimo...", width=250, height=35)

    if vartxt_senha_padrao != None and vartxt_val_max != "":
        entry_senha_padrao = ctk.CTkEntry(ajustes_frame, textvariable=vartxt_senha_padrao,
                                          placeholder_text="Digite a senha padrão...", width=250, height=35)
    else:
        entry_senha_padrao = ctk.CTkEntry(
            ajustes_frame, placeholder_text="Digite a senha padrão...", width=200, height=35)

    if vartxt_senha_saque != None and vartxt_senha_saque != "":
        entry_senha_saque = ctk.CTkEntry(ajustes_frame, textvariable=vartxt_senha_saque,
                                         placeholder_text="Digite a senha para saques...", width=250, height=35)
    else:
        entry_senha_saque = ctk.CTkEntry(
            ajustes_frame, placeholder_text="Digite a senha para saques...", width=250, height=35)
    if vartxt_site != None and vartxt_site != "":
        entry_site = ctk.CTkEntry(ajustes_frame, textvariable=vartxt_site,
                                  placeholder_text="Digite a URL da casa de apostas...", width=420, height=40)
    else:
        entry_site = ctk.CTkEntry(
            ajustes_frame, placeholder_text="Digite a URL da casa de apostas...", width=420, height=40)
    dropbox_games = ctk.CTkComboBox(button_group_frame, variable=ctk.StringVar(
        value=""), values=list_games, width=240, height=40)

    if bool_checkbox_mobile == None and bool_checkbox_mobile == "":
        bool_checkbox_mobile = ctk.BooleanVar(value= True)
    
    if bool_checkbox_ecoproxy == None and bool_checkbox_ecoproxy == "":
        bool_checkbox_ecoproxy = ctk.BooleanVar(value= True)
    if bool_checkbox_senha_rand == None and bool_checkbox_senha_rand == "":
        bool_checkbox_senha_rand = ctk.BooleanVar(value= True)
    if bool_checkbox_tempoCriacao_rand == None and bool_checkbox_tempoCriacao_rand == "":
        bool_checkbox_tempoCriacao_rand = ctk.BooleanVar(value= True)
    if bool_checkbox_senha_saque_random == None and bool_checkbox_senha_saque_random == "":
        bool_checkbox_senha_saque_random = ctk.BooleanVar(value= True)
    if bool_checkbox_usuarioNumero_rand == None and bool_checkbox_usuarioNumero_rand == "":
        bool_checkbox_usuarioNumero_rand = ctk.BooleanVar(value= True)
    
        
    # Deixando a tela de ajustes como primeira a ser exibida
    show_frame(button_group_frame, button_button_group)

##################################################################################################################################################
##################################################################################################################################################
    # GRUPO Ajustes

    # Configurar as colunas do grid para que se ajustem ao tamanho da tela
    ajustes_frame.grid_columnconfigure(0, weight=1)  # Coluna 0 ajustável
    ajustes_frame.grid_columnconfigure(1, weight=1)  # Coluna 1 ajustável

    # Campo e etiqueta para digitar valor maximo de depositos
    ctk.CTkLabel(ajustes_frame, text="Valor máximo de depósito:",  text_color="white", font=(
        "arial bold", 16)).grid(column=0, row=0, padx=40, pady=10, sticky="w")
    entry_val_max.grid(column=0, row=1, padx=40, pady=0, sticky="w")

    # Campo e etiqueta para digitar valor minimo de depositos
    ctk.CTkLabel(ajustes_frame, text="Valor mínimo de depósito:",  text_color="white", font=(
        "arial bold", 16)).grid(column=1, row=0, padx=10, pady=10, sticky="w")
    entry_val_min.grid(column=1, row=1, padx=10, pady=0, sticky="w")

    # Campo e etiqueta para senhas padrao de cadastro
    ctk.CTkLabel(ajustes_frame, text="Senha padrão:",  text_color="white", font=("arial bold", 16)).grid(column=0, row=2, padx=40, pady=10, sticky="w")
    entry_senha_padrao.grid(column=0, row=3, padx=40, pady=0, sticky="w")

    # Campo e etiqueta para senhas padrao de saques
    ctk.CTkLabel(ajustes_frame, text="Senha padrão de saque:",  text_color="white", font=("arial bold", 16)).grid(column=1, row=2, padx=10, pady=10, sticky="w")
    entry_senha_saque.grid(column=1, row=3, padx=10, pady=0, sticky="w")

    # Campos para digitar o site
    ctk.CTkLabel(ajustes_frame, text="Site da casa:",  text_color="white", font=("arial bold", 16)).grid(column=0, row=5, padx=40, pady=10, sticky="w")
    entry_site.grid(column=0, row=5, padx=165, pady=10, sticky="e", columnspan=2)

    # Etiqueta e dropbox da quantidade de telas.
    ctk.CTkLabel(ajustes_frame, text="Quantidade de telas:",  text_color="white", font=("arial bold", 16)).grid(column=0, row=6, padx=40, pady=10, sticky="w")
    
    
    options_qtd_loop = ctk.CTkOptionMenu(ajustes_frame, values=["5", "10", "2", "3", "4", "6", "7", "8", "9", "1"], width=150, height=40, variable=ctk.StringVar(value= qdt_loop.replace("qdt_loop=", "")))
    options_qtd_loop.grid(column=0, row=7, padx=40, pady=0, sticky="w")

    # Dropdown para selecionar o tipo da chave pix.
    ctk.CTkLabel(ajustes_frame, text="Tipo da chave PIX:",  text_color="white", font=("arial bold", 16)).grid(column=0, row=6, padx=240, pady=10, sticky="w", columnspan=2)
    dropbox_modelo_pix = ctk.CTkOptionMenu(ajustes_frame, values=["Email", "CPF", "Telefone", "EVC"], variable= ctk.StringVar(value= modelo_pix.replace("modelo_pix=", "")),width=150, height=40)
    dropbox_modelo_pix.grid(column=0, row=7, padx=240, pady=10, sticky="w", columnspan=2)

    # Dropbox e Etiqueta para selecionar o tipo da casa.
    ctk.CTkLabel(ajustes_frame, text="Tipo da casa:",  text_color="white", font=("arial bold", 14)).grid(column=1, row=6, padx=20, pady=10, sticky="w", columnspan=2)
    options_type_house = ctk.CTkOptionMenu(ajustes_frame, values=["Casa 1", "Casa 2", "Casa 3"], width=200, height=40)
    options_type_house.grid(column=1, row=7, padx=20, pady=10, sticky="w", columnspan=2)

    # Selecionar planilha base etiqueta + botao
    # Colocar no final junto com o save
    # ctk.CTkLabel(ajustes_frame, text="Defina a planilha base:",  text_color="white", font=("arial bold", 14)).grid(column= 0, row= 0, padx = 0, pady = 20)
    # ctk.CTkButton(ajustes_frame, textvariable=var_caminho_planilha, command=escolher_planilha, width=100, height=40).grid(column= 1, row= 8, padx = 20, pady = 10)


    checkbox_mobile = ctk.CTkCheckBox(ajustes_frame, text="MOBILE", variable=bool_checkbox_mobile, onvalue=True, offvalue=False).grid(column=0, row=8, padx=40, pady=10, sticky="w", columnspan=2)

    # Checkbox modo Random senha login
    checkbox_senha_rand = ctk.CTkCheckBox(ajustes_frame, text="SENHA RANDOM", variable=bool_checkbox_senha_rand, onvalue=True, offvalue=False).grid(column=0, row=8, padx=240, pady=10, sticky="w", columnspan=2)

    # Criando a Random Senha de saque
    checkbox_senha_saque_random = ctk.CTkCheckBox(ajustes_frame, text="SENHA SAQUE RANDOM", variable=bool_checkbox_senha_saque_random, onvalue=True, offvalue=False).grid(column=1, row=8, padx=20, pady=10, sticky="w", columnspan=2)

    # Checkbox modo ECO PROXY
    checkbox_ecoproxy = ctk.CTkCheckBox(ajustes_frame, text="ECO PROXY", variable=bool_checkbox_ecoproxy, onvalue=True, offvalue=False).grid(column=0, row=9, padx=40, pady=10, sticky="w", columnspan=2)

    # Checkbox modo Random senha login
    checkbox_usuarioNumero_rand = ctk.CTkCheckBox(ajustes_frame, text="USUARIO SEM NUMERO", variable=bool_checkbox_usuarioNumero_rand, onvalue=True, offvalue=False).grid(column=0, row=9, padx=240, pady=10, sticky="w", columnspan=2)

    # Criando a Random Senha de saque
    checkbox_tempoCriacao_rand = ctk.CTkCheckBox(ajustes_frame, text="TEMPO PRA CRIACAO", variable=bool_checkbox_tempoCriacao_rand, onvalue=True, offvalue=False).grid(column=1, row=9, padx=20, pady=10, sticky="w", columnspan=2)

    # Selecionar planilha base etiqueta + botao
    # Colocar no final junto com o save
    # ctk.CTkLabel(ajustes_frame, text="Defina a planilha base:",  text_color="white", font=("arial bold", 14)).grid(column= 0, row= 0, padx = 0, pady = 20)
    ctk.CTkButton(ajustes_frame, textvariable=var_caminho_planilha, command=escolher_planilha, width=250, height=40).grid(column= 0, row= 10, padx = 40, pady = 20, sticky="w")

    # # Selecionar planilha base etiqueta + botao
    # #ctk.CTkLabel(button_group_frame, text="Clique para salvar as informações:",  text_color="white", font=("arial bold", 14)).grid(column= 0, row= 1, padx = 20, pady = 0)
    ctk.CTkButton(ajustes_frame, text="Salvar Infos", command=atualizar_infos, width=250, height=40).grid(column= 1, row= 10, padx = 0, pady = 20, sticky="w")

##################################################################################################################################################
##################################################################################################################################################
    # GRUPO BOTÕES

    # # Etiqueta e dropbox dos jogos cadastrados.
    ctk.CTkLabel(button_group_frame, text="Nome do jogo a ser pesquisado:",  text_color="white", font=("arial bold", 16)).grid(column = 0, row = 1, padx=40, pady=10,sticky=W)
    dropbox_games.grid(column = 0, row = 2, padx=40, pady=0, sticky=W)
    ctk.CTkButton(button_group_frame, text="+", command=add_game, width=30, height=40).grid(column=1, row=2, pady=0, padx=(0, 40), sticky = W)
    ctk.CTkButton(button_group_frame, text="-", command=remove_game, width=30, height=40).grid(column=1, row=2, pady=0, padx=(40, 0), sticky = W)

    # Botao para abrir a automacao.
    ctk.CTkButton(button_group_frame, text="Iniciar Navegadores", command=iniciar_navegadores, width=250, height=40).grid(column= 0, row= 3, padx = 40, pady = 20)
    # Botao para pesquisar jogo
    ctk.CTkButton(button_group_frame, text="Pesquisar Game", command=ativar_jogar, width=250, height=40).grid(column= 1, row= 3, padx = 20, pady = 20)

    # Botao para cadastrar chave PIX
    ctk.CTkButton(button_group_frame, text="Cadastrar PIX", command=ativar_cadastrar_pix, width=250, height=40).grid(column= 0, row= 4, padx = 40, pady = 20)
    # Botao para sacar completo
    ctk.CTkButton(button_group_frame, text="Sacar Completo", command=ativar_sacar_completo, width=250, height=40).grid(column= 1, row= 4, padx = 20, pady = 20)

    # Botao para depositar
    ctk.CTkButton(button_group_frame, text="Depositar", command=ativar_depositar, width=250, height=40).grid(column= 0, row= 5, padx = 40, pady = 20)
    # Botao para coletar Bonus
    ctk.CTkButton(button_group_frame, text="Coletar Bonus", command=ativar_coletar_bonus, width=250, height=40).grid(column= 1, row= 5, padx = 20, pady = 20)

    # Botao para digitar as chaves PIX.
    ctk.CTkButton(button_group_frame, text="Digitar Chaves", command=ativar_cadastrar_pix, width=250, height=40).grid(column= 0, row= 5, padx = 40, pady = 20)
    # Botao para fechar as paginas abertas.
    ctk.CTkButton(button_group_frame, text="Fechar Paginas", command=fechar_abas, width=250, height=40).grid(column= 1, row= 5, padx = 20, pady = 20)

    # # Casa 1 = Casa comum
    # # Casa 2 = Casa so o numero
    # # Casa 3 = Casa comum versao 2

    janela.mainloop()

async def check_for_updates():
    # Verifica se o lock de atualização existe para evitar repetição
    if os.path.exists(UPDATE_LOCK):
        with open(UPDATE_LOCK) as lock_file:
            last_update = datetime.strptime(lock_file.read().strip("last_update:"), "%Y-%m-%dT%H:%M:%S")
            if last_update > datetime.now() - timedelta(hours=1):
                print("Atualização já realizada recentemente.")
                main()

    try:
        os.makedirs("temp", exist_ok=True)
        print("Baixando atualização...")
        wget.download(UPDATE_URL, TEMP_DOWNLOAD_PATH)
        print("\nAtualização baixada com sucesso.")
        
        await apply_update()
        
    except Exception as ex:
        print("Erro ao baixar atualização:", ex)
        sys.exit()

async def apply_update():
    try:
        if os.path.exists(LOCAL_EXECUTABLE):
            os.remove(LOCAL_EXECUTABLE)
        
        shutil.move(TEMP_DOWNLOAD_PATH, LOCAL_EXECUTABLE)
        print("Aplicação atualizada com sucesso.")
        
        # Cria o arquivo de lock para sinalizar que a atualização foi feita
        with open(UPDATE_LOCK, 'w') as lock_file:
            lock_file.write("last_update:" + datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        
        restart_application()  # Chama a funço normalmente
        
    except Exception as ex:
        print("Erro ao aplicar a atualização:", ex)
        sys.exit()

def restart_application():
    try:
        print("Reiniciando a aplicação...")
        # Substitui o processo atual pelo novo executável
        sys.stdout.flush()
        os.execv(LOCAL_EXECUTABLE, [LOCAL_EXECUTABLE] + sys.argv[1:])
    except Exception as ex:
        print("Erro ao reiniciar a aplicação:", ex)
        sys.exit()

def main():
    acesso, mensagem = consultar_permissao_computador()
    if acesso:
        app_principal()
    else:
        login_app()

# Verifica por atualizações no início do programa
asyncio.run(check_for_updates())