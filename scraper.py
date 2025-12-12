import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def obtener_driver():
    """Configura el navegador Chrome detectando si es Local o Render"""
    chrome_options = Options()
    
    # Opciones obligatorias para servidores (Render)
    chrome_options.add_argument("--headless")  # Ojo: En tu PC también correrá sin ventana. Si quieres verla, comenta esto.
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Detección de entorno RENDER
    chrome_bin = os.environ.get("CHROME_BIN")
    
    if chrome_bin:
        # ESTAMOS EN RENDER
        chrome_options.binary_location = chrome_bin
        driver = webdriver.Chrome(options=chrome_options)
    else:
        # ESTAMOS EN TU PC (Windows/Mac)
        # Instala el driver automáticamente
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
    return driver

def consultar_multa(dni):
    driver = None
    mensaje = "Error desconocido"
    
    try:
        driver = obtener_driver()
        # URL DEL JNE (Verifica que sea la actual)
        driver.get("https://plataformaelectoral.jne.gob.pe/multas-electorales/consultar")
        
        wait = WebDriverWait(driver, 10)
        
        # --- LÓGICA DE SCRAPING ---
        # 1. Encontrar campo DNI
        # NOTA: Los IDs ("txtDni", etc) deben ser verificados en la web real con F12
        input_dni = wait.until(EC.presence_of_element_located((By.ID, "txtDni")))
        input_dni.clear()
        input_dni.send_keys(dni)
        
        # 2. Encontrar botón buscar y dar clic
        btn_buscar = driver.find_element(By.ID, "btnConsultar")
        btn_buscar.click()
        
        # 3. Esperar resultado
        time.sleep(2) # Espera de seguridad
        
        # Aquí intentamos capturar el resultado. 
        # Modifica este XPATH o ID según lo que salga en la web del JNE
        # Esto es un ejemplo genérico:
        try:
            resultado_element = driver.find_element(By.CLASS_NAME, "resultado-busqueda") # <--- AJUSTAR ESTO
            mensaje = resultado_element.text
        except:
            mensaje = "Consulta realizada (No se pudo leer el texto específico, revisa los selectores)"

    except Exception as e:
        mensaje = f"Ocurrió un error: {str(e)}"
    finally:
        if driver:
            driver.quit()
            
    return mensaje