import os
import sys
import psutil
import logging
import wget
import shutil
import subprocess
import threading
import requests
from datetime import datetime
import customtkinter as ctk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

REPO_OWNER = "theuldev"
REPO_NAME = "toProfit"
FILE_PATH = "Toprofit.exe"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits?path={FILE_PATH}"

LOCAL_DIRECTORY = "."
TEMP_DOWNLOAD_PATH = "temp/Toprofit-latest.exe"
LOCAL_EXECUTABLE = os.path.join(os.getcwd(), "Toprofit.exe")
LAST_COMMIT_FILE = "last_commit.txt"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def create_commit_file_if_not_exists():
    if not os.path.exists(LAST_COMMIT_FILE):
        try:
            with open(LAST_COMMIT_FILE, "w") as file:
                file.write("")
            logging.info(f"Arquivo {LAST_COMMIT_FILE} criado com sucesso.")
        except Exception as ex:
            logging.error(f"Erro ao criar o arquivo {LAST_COMMIT_FILE}: {ex}")

def get_remote_commit_date():
    try:
        logging.info("Consultando o GitHub para obter informações do commit...")
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        commits = response.json()

        if commits:
            commit_date = commits[0]["commit"]["committer"]["date"]
            return datetime.fromisoformat(commit_date.replace("Z", "+00:00")).replace(tzinfo=None)
        else:
            logging.warning("Nenhum commit encontrado para o arquivo especificado.")
            return None
    except Exception as ex:
        logging.error(f"Erro ao consultar o GitHub: {ex}")
        return None

def get_local_commit_date():
    create_commit_file_if_not_exists()

    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, "r") as file:
            try:
                commit_date = file.read().strip()
                return datetime.fromisoformat(commit_date) if commit_date else None
            except ValueError:
                logging.warning("Formato de data inválido no arquivo local.")
    return None

def update_commit_file(commit_date):
    try:
        with open(LAST_COMMIT_FILE, "w") as file:
            file.write(commit_date.isoformat())
        logging.info(f"Arquivo {LAST_COMMIT_FILE} atualizado com a nova data de commit.")
    except Exception as ex:
        logging.error(f"Erro ao atualizar o arquivo {LAST_COMMIT_FILE}: {ex}")

def close_updater():
    logging.info("Fechando o atualizador...")
    app.quit()
    sys.exit()

def start_thread(function):
    thread = threading.Thread(target=function)
    thread.start()
    return thread

def check_for_updates():
    remote_date = get_remote_commit_date()
    local_date = get_local_commit_date()

    if not remote_date:
        logging.error("Não foi possível obter a data do commit remoto.")
        return

    if not local_date or remote_date > local_date:
        logging.info("Nova versão disponível. Atualizando...")  
        update_commit_file(remote_date)
        start_download()
    else:
        logging.info("Você já está na versão mais recente.")
        start_thread(run_application)
        close_updater()

def download_callback(current, total, bar):
    if total > 0:
        percent = current / total
        progress_bar.set(percent)
        status_label.configure(text=f"Baixando... {int(percent * 100)}%")

def download_update(event):
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
        event.set()
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

def run_application():
    if os.path.exists(LOCAL_EXECUTABLE):
        process = subprocess.Popen(LOCAL_EXECUTABLE, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logging.info("Processo iniciado.")
        
        while not is_process_running("Toprofit.exe"):
            time.sleep(0.1) 
        
        logging.info("O processo foi iniciado.")
        close_updater() 
    else:
        logging.error("O executável não existe: %s", LOCAL_EXECUTABLE)
        sys.exit()

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            return True
    return False

def start_download():
    status_label.configure(text="Iniciando download...")
    update_event = threading.Event()
    threading.Thread(target=download_update, args=(update_event,)).start()

    update_event.wait()
    close_updater()

app = ctk.CTk()
app.title("ToProfit")
app.geometry("400x300")

title_label = ctk.CTkLabel(app, text="Atualizador de Software", font=("Arial", 18))
title_label.pack(pady=20)

status_label = ctk.CTkLabel(app, text="Verificando atualizações...", font=("Arial", 14))
status_label.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.pack(pady=20)
progress_bar.set(0)

threading.Thread(target=check_for_updates).start()

app.mainloop()
