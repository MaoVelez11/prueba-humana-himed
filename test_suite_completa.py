from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuración Maestra (se ejecuta una sola vez) ---
# Asegúrate de que 'chromedriver.exe' esté en la misma carpeta que este script
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
# Se crea un objeto de espera que se usará en todo el script. Esperará un máximo de 15 segundos.
wait = WebDriverWait(driver, 15) 
print("✅ NAVEGADOR INICIADO PARA LA SUITE DE PRUEBAS COMPLETA")
driver.maximize_window()

# --- Inicio de la Suite de Pruebas ---
try:
    # ==================================================================
    #                      INICIO FLUJO 1: LOGIN
    # ==================================================================
    print("\n▶️  Iniciando Flujo 1: Prueba de Login Fallido...")
    
    # 1.1. Abrimos la página de RIPS
    driver.get("https://medsas.co/modulo-de-rips/")
    print("   - Página de RIPS abierta.")
    
    # 1.2. Clic para ir a HiMed Web (abre una nueva pestaña)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ingresar a HiMed Web"))).click()
    wait.until(EC.number_of_windows_to_be(2))
    # Cambiamos el control a la nueva pestaña (la segunda en la lista)
    driver.switch_to.window(driver.window_handles[1])
    print(f"   - Foco cambiado a la pestaña de login: {driver.current_url}")
    time.sleep(2)

    # 1.3. Rellenamos el formulario de login con datos inválidos
    wait.until(EC.element_to_be_clickable((By.ID, "nit_cc"))).send_keys("123456789")
    driver.find_element(By.ID, "idV").send_keys("usuario_invalido")
    driver.find_element(By.ID, "contrasenaV").send_keys("clave_incorrecta")
    driver.find_element(By.NAME, "login").click()
    print("   - Formulario de login enviado con datos incorrectos.")
    time.sleep(2)
    
    
    # 1.5. Limpieza: Cerramos la pestaña de login y volvemos a la pestaña principal
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("   - Pestaña de login cerrada. Volviendo a la pestaña principal.")
    print("⏹️  Flujo 1: FINALIZADO CON ÉXITO")
    time.sleep(2)
    # ==================================================================
    #                      INICIO FLUJO 2: COMPRA
    # ==================================================================
    print("\n▶️  Iniciando Flujo 2: Prueba de Compra y Cancelación...")

    # Forzamos la recarga de la página para asegurar un estado limpio
    print("   - Recargando la página para iniciar el flujo de compra.")
    driver.get("https://medsas.co/modulo-de-rips/")
    time.sleep(2)

    # 2.1. Desde la página RIPS, hacemos clic en "Comprar ahora"
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Comprar ahora"))).click()
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    print(f"   - Foco cambiado a la pestaña de producto: {driver.current_url}")
    time.sleep(2)
    
    # 2.2. Cambiamos la cantidad a 7, añadimos al carrito y vamos a pagar
    campo_cantidad = wait.until(EC.visibility_of_element_located((By.NAME, "quantity")))
    campo_cantidad.clear()
    campo_cantidad.send_keys("7")
    wait.until(EC.element_to_be_clickable((By.NAME, "add-to-cart"))).click()
    print("   - Producto añadido al carrito con cantidad 7.")
    wait.until(EC.element_to_be_clickable((By.ID, "PayButton"))).click()
    print(f"   - Navegado a la página del carrito: {driver.current_url}")
    time.sleep(2)

    # 2.3. Eliminamos el producto y verificamos que el carrito quede vacío
    print(f"7. Navegado a la página del carrito: {driver.current_url}")
    eliminar_item_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "remove")))
    eliminar_item_btn.click()
    print("8. Clic en 'x' para eliminar el producto del carrito.")
    

    # 2.4. Volvemos a la página de inicio usando el botón del menú
    inicio_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inicio")))
    inicio_btn.click()
    print("   - Clic en el botón 'Inicio' del menú.")

    # 2.5. Verificamos que la URL actual sea la de la página de inicio
    wait.until(EC.url_to_be("https://medsas.co/"))
    assert driver.current_url == "https://medsas.co/"
    print("   - Verificación de regreso a página de inicio: CORRECTA.")
    print("⏹️  Flujo 2: FINALIZADO CON ÉXITO")
    time.sleep(2)

    # ==================================================================
    #                      INICIO FLUJO 3: CICLO
    # ==================================================================
    print("\n▶️  Iniciando Flujo 3: Regreso al punto de partida...")
    driver.get("https://medsas.co/modulo-de-rips/")
    # Esperamos a que un elemento clave de la página esté visible para confirmar la navegación
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Ingresar a HiMed Web")))
    print("   - Navegado de vuelta a la página de RIPS.")
    print("⏹️  Flujo 3: FINALIZADO CON ÉXITO")

    print("\n✅✅✅ ¡SUITE DE PRUEBAS COMPLETA EJECUTADA EXITOSAMENTE! ✅✅✅")

finally:
    # Este bloque se ejecuta siempre, incluso si hay un error, para cerrar el navegador.
    print("\nCerrando el navegador en 5 segundos...")
    time.sleep(5)
    driver.quit()
    print("Prueba finalizada.")