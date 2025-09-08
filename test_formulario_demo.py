from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuración inicial ---
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
# Aumentamos el tiempo de espera implícito por si acaso
driver.implicitly_wait(5) 

# --- Inicio de la prueba ---
try:
    # 1. Abrimos la página inicial
    driver.get("https://medsas.co/modulo-de-rips/")
    driver.maximize_window()
    print("1. Página inicial abierta.")

    # 2. Clic en el botón para ir al login
    # Usamos una espera explícita también para este botón inicial
    wait = WebDriverWait(driver, 10)
    boton_ingresar_himed = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ingresar a HiMed Web")))
    boton_ingresar_himed.click()
    print("2. Clic en 'Ingresar a HiMed Web'.")

    # 3. Manejo de la nueva pestaña
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    print(f"3. Foco cambiado a la nueva pestaña: {driver.current_url}")

    # ------------------- CAMBIO MÁS IMPORTANTE AQUÍ -------------------
    # Ahora esperamos a que los campos estén listos para ser clickeados
    print("4. Esperando a que el campo NIT esté listo para interactuar...")
    campo_nit = wait.until(EC.element_to_be_clickable((By.ID, "nit_cc")))
    
    print("5. Esperando a que el campo Usuario esté listo para interactuar...")
    campo_usuario = wait.until(EC.element_to_be_clickable((By.ID, "idV")))
    
    print("6. Esperando a que el campo Contraseña esté listo para interactuar...")
    campo_contrasena = wait.until(EC.element_to_be_clickable((By.ID, "contrasenaV")))
    
    print("   -> ¡Todos los campos de texto están listos!")
    # ------------------------------------------------------------------

    # 7. Rellenamos el formulario, haciendo clic primero
    print("7. Procediendo a rellenar el formulario:")
    
    print("   - Escribiendo en NIT...")
    campo_nit.click()
    campo_nit.send_keys("123456789")
    
    print("   - Escribiendo en Usuario...")
    campo_usuario.click()
    campo_usuario.send_keys("usuario_invalido")
    
    print("   - Escribiendo en Contraseña...")
    campo_contrasena.click()
    campo_contrasena.send_keys("clave_incorrecta")
    
    print("   -> Formulario rellenado.")
    time.sleep(1) # Pausa visual

    # 8. Hacemos clic en el botón de Ingresar
    print("8. Buscando y haciendo clic en el botón 'Ingresar'.")
    boton_ingresar = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
    boton_ingresar.click()

    # 9. Verificamos el mensaje de error
    print("9. Esperando el mensaje de error...")
    mensaje_error = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))
    
    texto_esperado = "Error! Usuario y/o contraseña incorrectos"
    print(f"   -> Mensaje encontrado: '{mensaje_error.text}'")
    
    assert texto_esperado in mensaje_error.text
    print("\n✅ ¡PRUEBA EXITOSA! El flujo de login fallido funciona como se esperaba.")

finally:
    # Cerramos el navegador
    print("\nCerrando el navegador en 5 segundos...")
    time.sleep(5)
    driver.quit()
    print("Prueba finalizada.")