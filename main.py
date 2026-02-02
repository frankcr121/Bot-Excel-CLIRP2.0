from playwright.sync_api import sync_playwright
from lib_resources.co_playwright import *
from lib_resources.co_sheets import *
from lib_resources.co_funciones import *
from lib_resources.co_proceso import *
#from lib_resources.co_conexion import DataBase
import time
#database = DataBase()

def run():
    hay_trabajo, datos, sheet = buscando_sheets()
    if not hay_trabajo:
        print(">>> NO SE ENCONTRÓ TRABAJO (Pendiente + Axional). Fin del proceso.")
        return
    trabajos_pendientes = filtrar_pendientes(datos)
    total_registros = len(trabajos_pendientes)
    if total_registros == 0:
        print(">>> No hay nada pendiente. Cerrando.")
        return

    with sync_playwright() as p:  
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://erp.crp.com.pe/")
        ver_logue = login_ERP(page)
        if ver_logue:
            print("Login Exitoso")
            
            principal(page, trabajos_pendientes, total_registros, sheet)
            
            #time.sleep(10000)
        browser.close()

if __name__ == "__main__":
    run()