import os
import sys
import psutil
import logging
import wget
import shutil
import subprocess
import re
import customtkinter as ctk
import threading
import requests
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL e repositório GitHub
REPO_OWNER = "theuldev"
REPO_NAME = "toProfit"
FILE_PATH = "Toprofit.exe"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={FILE_PATH}"

LOCAL_DIRECTORY = "."
TEMP_DOWNLOAD_PATH = "temp/Toprofit-latest.exe"
LOCAL_EXECUTABLE = os.path.join(os.getcwd(), "Toprofit.exe")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def get_remote_commit_date():
    """Obtém a data do último commit associado ao arquivo remoto no GitHub."""
    try:
        logging.info("Consultando o GitHub para obter informações do commit...")
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        commits = response.json()

        if commits:
            commit_date = commits[0]["commit"]["committer"]["date"]
            return datetime.fromisoformat(commit_date.replace("Z", "+00:00"))
        else:
            logging.warning("Nenhum commit encontrado para o arquivo especificado.")
            return None
    except Exception as ex:
        logging.error(f"Erro ao consultar o GitHub: {ex}")
        return None

def get_local_file_date():
    """Obtém a data da última modificação do executável local."""
    if os.path.exists(LOCAL_EXECUTABLE):
        return datetime.fromtimestamp(os.path.getmtime(LOCAL_EXECUTABLE))
    else:
        logging.warning("Arquivo local não encontrado.")
        return None

def check_for_updates():
    """Verifica se há atualizações baseadas na data do commit."""
    remote_date = get_remote_commit_date()
    local_date = get_local_file_date()

    if not remote_date:
        logging.error("Não foi possível obter a data do commit remoto.")
        return

    if not local_date or remote_date > local_date:
        logging.info("Nova versão disponível. Atualizando...")
        start_download()
    else:
        logging.info("Você já está na versão mais recente.")
        run_application(LOCAL_EXECUTABLE)

def download_callback(current, total, bar):
    if total > 0:
        percent = current / total
        progress_bar.set(percent)
        status_label.configure(text=f"Baixando... {int(percent * 100)}%")

def download_update():
    try:
        os.makedirs("temp", exist_ok=True)
        logging.info("Baixando atualização...")
        wget.download(
            f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/{FILE_PATH}?raw=true",
            TEMP_DOWNLOAD_PATH,
            bar=download_callback
        )
        logging.info("Atualização baixada com sucesso.")
        apply_update()
    except Exception as ex:
        logging.error("Erro ao baixar atualização: %s", ex)
        sys.exit()

def apply_update():
    try:
        terminate_existing_processes()
        if os.path.exists(LOCAL_EXECUTABLE):
            logging.info("Deletando o executável antigo...")
            os.remove(LOCAL_EXECUTABLE)

        shutil.move(TEMP_DOWNLOAD_PATH, LOCAL_EXECUTABLE)
        logging.info("Aplicação atualizada com sucesso.")
        restart_application()
    except Exception as ex:
        logging.error("Erro ao aplicar a atualização: %s", ex)
        sys.exit()

def terminate_existing_processes():
    for proc in psutil.process_iter():
        try:
            if proc.name() == os.path.basename(LOCAL_EXECUTABLE):
                logging.info("Finalizando o processo anterior...")
                proc.terminate()
                proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logging.warning("Não foi possível finalizar o processo: %s", proc)

def restart_application():
    try:
        logging.info("Reiniciando a aplicação...")
        if os.path.exists(LOCAL_EXECUTABLE):
            app.withdraw()
            subprocess.Popen([LOCAL_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)
            logging.info("A aplicação foi reiniciada com sucesso.")
        else:
            logging.error("O executável não foi encontrado após a atualização.")
        sys.exit()
    except Exception as ex:
        logging.error("Erro ao reiniciar a aplicação: %s", ex)
        sys.exit()

def run_application(executable_path):
    if os.path.exists(executable_path):
        os.system(executable_path)
        sys.exit()
    else:
        logging.error("O executável não existe: %s", executable_path)
        sys.exit()

# Interface gráfica
def start_download():
    status_label.configure(text="Iniciando download...")
    threading.Thread(target=download_update).start()

app = ctk.CTk()
app.title("Atualizador de Software")
app.geometry("400x300")

title_label = ctk.CTkLabel(app, text="Atualizador de Software", font=("Arial", 18))
title_label.pack(pady=20)

status_label = ctk.CTkLabel(app, text="Verificando atualizações...", font=("Arial", 14))
status_label.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.pack(pady=20)
progress_bar.set(0)

# Inicia a verificação de atualizações assim que a aplicação abre
threading.Thread(target=check_for_updates).start()

app.mainloop()
