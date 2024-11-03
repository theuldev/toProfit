import os
import sys
import psutil
import logging
import wget
import shutil
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

UPDATE_URL = "https://github.com/theuldev/toProfit/blob/main/Toprofit-v3.1.exe?raw=true"
LOCAL_EXECUTABLE = "Toprofit-v3.0.exe" 
TEMP_DOWNLOAD_PATH = "temp/Toprofit-latest.exe" 
CURRENT_VERSION = "v3.0" 
NEW_LOCAL_EXECUTABLE = "Toprofit-v3.1.exe" 
def check_for_updates():
    remote_version = "v3.1"  

    if remote_version > CURRENT_VERSION:
        logging.info(f"Nova versão disponível: {remote_version}. Atualizando...")
        download_update()
    else:
        logging.info("Você já está na versão mais recente.")
        run_application()

def download_update():
    try:
        os.makedirs("temp", exist_ok=True)
        logging.info("Baixando atualização...")
        wget.download(UPDATE_URL, TEMP_DOWNLOAD_PATH)
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

        shutil.move(TEMP_DOWNLOAD_PATH, NEW_LOCAL_EXECUTABLE)
        logging.info("Aplicação atualizada com sucesso.")
        restart_application()
        
    except Exception as ex:
        logging.error("Erro ao aplicar a atualização: %s", ex)
        sys.exit()

def terminate_existing_processes():
    """Finaliza qualquer processo existente do executável."""
    for proc in psutil.process_iter():
        try:
            if proc.name() == LOCAL_EXECUTABLE:
                logging.info("Finalizando o processo anterior...")
                proc.terminate()
                proc.wait()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            logging.warning("Não foi possível finalizar o processo: %s", proc)

def restart_application():
    try:
        logging.info("Reiniciando a a6plicação...")
        process = subprocess.Popen([NEW_LOCAL_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)
        process.wait()
        logging.info("A aplicação foi reiniciada com sucesso.")
        sys.exit()
    except Exception as ex:
        logging.error("Erro ao reiniciar a aplicação: %s", ex)
        sys.exit()

def run_application():
    """Executa o aplicativo atual."""
    process = subprocess.Popen([NEW_LOCAL_EXECUTABLE], creationflags=subprocess.CREATE_NEW_CONSOLE)
    process.wait()
    sys.exit()

if __name__ == "__main__":
    check_for_updates()