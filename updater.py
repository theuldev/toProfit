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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

UPDATE_URL = "https://github.com/theuldev/toProfit/blob/main/Toprofit-v3.1.exe?raw=true"
LOCAL_DIRECTORY = "." 
TEMP_DOWNLOAD_PATH = "temp/Toprofit-latest.exe" 
NEW_LOCAL_EXECUTABLE = "Toprofit-v3.1.exe"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Funções do processo de atualização
def find_executable_with_version(directory, version_pattern):
    for filename in os.listdir(directory):
        if re.search(version_pattern, filename):
            return os.path.join(directory, filename)
    return None

def check_for_updates():
    local_executable = find_executable_with_version(LOCAL_DIRECTORY, r"Toprofit-v(\d+\.\d+)\.exe")
    if not local_executable:
        logging.error("Executável local não encontrado.")
        return
    
    local_version = get_version_from_filename(local_executable)
    remote_version = "3.1"

    if local_version and remote_version > local_version:
        logging.info(f"Nova versão disponível: {remote_version}. Atualizando...")
        start_download()
    else:
        logging.info("Você já está na versão mais recente.")
        run_application(local_executable)

def get_version_from_filename(filename):
    match = re.search(r"v(\d+\.\d+)", filename)
    if match:
        return match.group(1)
    return None

def download_callback(current, total, bar):
    if total > 0:
        percent = current / total
        progress_bar.set(percent)
        status_label.configure(text=f"Baixando... {int(percent * 100)}%")

def download_update():
    try:
        os.makedirs("temp", exist_ok=True)
        logging.info("Baixando atualização...")
        wget.download(UPDATE_URL, TEMP_DOWNLOAD_PATH, bar=download_callback)
        logging.info("Atualização baixada com sucesso.")
        apply_update()
    except Exception as ex:
        logging.error("Erro ao baixar atualização: %s", ex)
        sys.exit()

def apply_update():
    try:
        terminate_existing_processes()
        if os.path.exists(NEW_LOCAL_EXECUTABLE):
            logging.info("Deletando o executável antigo...")
            os.remove(NEW_LOCAL_EXECUTABLE)

        shutil.move(TEMP_DOWNLOAD_PATH, NEW_LOCAL_EXECUTABLE)
        logging.info("Aplicação atualizada com sucesso.")
        restart_application()
    except Exception as ex:
        logging.error("Erro ao aplicar a atualização: %s", ex)
        sys.exit()

def terminate_existing_processes():
    for proc in psutil.process_iter():
        try:
            if proc.name() == NEW_LOCAL_EXECUTABLE:
                logging.info("Finalizando o processo anterior...")
                proc.terminate()
                proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logging.warning("Não foi possível finalizar o processo: %s", proc)

def restart_application():
    try:
        logging.info("Reiniciando a aplicação...")
        if os.path.exists(NEW_LOCAL_EXECUTABLE):
            process = subprocess.Popen([NEW_LOCAL_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)
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

threading.Thread(target=check_for_updates).start()

app.mainloop()
