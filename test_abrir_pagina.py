# 1. Importamos lo que necesitamos de la librería Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# 2. Le decimos a Selenium dónde está nuestro controlador (chromedriver)
# Como lo pusimos en la misma carpeta, solo necesitamos el nombre del archivo.
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 3. La acción principal: abrir la URL
print("Abriendo la página de Medsas...")
driver.get("https://medsas.co/modulo-de-rips/")

# 4. Verificación simple: obtenemos el título de la página y lo imprimimos
titulo_pagina = driver.title
print(f"El título de la página es: '{titulo_pagina}'")

# 5. Una pausa para que podamos ver qué pasó
time.sleep(5) # Espera 5 segundos

# 6. Cerramos el navegador para terminar la prueba
driver.quit()
print("Prueba finalizada. El navegador se ha cerrado.")