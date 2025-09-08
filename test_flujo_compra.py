from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuración inicial ---
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
# Aumentamos el tiempo máximo de espera para las esperas explícitas
wait = WebDriverWait(driver, 15) # Esperará hasta 15 segundos

# --- Inicio de la prueba ---
try:
    # 1. Abrimos la página inicial
    driver.get("https://medsas.co/modulo-de-rips/")
    driver.maximize_window()
    print("1. Página inicial abierta.")

    # 2. Hacemos clic en "Comprar ahora"
    # Este botón nos llevará a una nueva pestaña
    comprar_ahora_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Comprar ahora")))
    comprar_ahora_btn.click()
    print("2. Clic en 'Comprar ahora'.")

    # 3. Cambiamos el foco a la nueva pestaña de producto
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])
    print(f"3. Foco cambiado a la nueva pestaña de producto: {driver.current_url}")

    # 4. Cambiamos la cantidad a 7
    # El ID de este campo puede cambiar, pero el 'name' es más estable
    campo_cantidad = wait.until(EC.visibility_of_element_located((By.NAME, "quantity")))
    campo_cantidad.clear() # Borramos el '1' que viene por defecto
    campo_cantidad.send_keys("7")
    print("4. Cantidad cambiada a 7.")

    # 5. Añadimos al carrito
    añadir_carrito_btn = wait.until(EC.element_to_be_clickable((By.NAME, "add-to-cart")))
    añadir_carrito_btn.click()
    print("5. Producto añadido al carrito.")

    # 6. Hacemos clic en "Pagar ahora"
    # Este botón aparece después de añadir al carrito, así que debemos esperarlo. Su ID es muy confiable.
    pagar_ahora_btn = wait.until(EC.element_to_be_clickable((By.ID, "PayButton")))
    print(f"6. Botón '{pagar_ahora_btn.text}' encontrado. Haciendo clic.")
    pagar_ahora_btn.click()
    
    # 7. Ya en la página del carrito, eliminamos el producto
    # Esperamos a que la página del carrito cargue y el botón de eliminar sea visible
    print(f"7. Navegado a la página del carrito: {driver.current_url}")
    eliminar_item_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "remove")))
    eliminar_item_btn.click()
    print("8. Clic en 'x' para eliminar el producto del carrito.")

    # 8. Verificamos que el carrito esté vacío
    # Esperamos a que aparezca el mensaje de "Tu carrito está vacío" para confirmar la eliminación.
    mensaje_carrito_vacio = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart-empty")))
    print(f"9. Verificación exitosa: '{mensaje_carrito_vacio.text}'")
    
    # 9. Volvemos al inicio haciendo clic en el logo
    # El botón que mencionaste no es un buen localizador. Es mucho más seguro y común
    # hacer clic en el logo de la empresa para volver al inicio.
    inicio_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Inicio")))
    inicio_btn.click()
    print("10. Clic en el logo para volver a la página de inicio.")

    # 10. ASERCIÓN FINAL: Verificamos que estamos en la página de inicio
    wait.until(EC.url_to_be("https://medsas.co/modulo-de-rips/"))
    print(f"11. Navegación final exitosa. URL actual: {driver.current_url}")
    assert driver.current_url == "https://medsas.co/modulo-de-rips/"
    
    print("\n✅ ¡PRUEBA DEL FLUJO DE COMPRA EXITOSA!")

finally:
    # Cerramos el navegador
    print("\nCerrando el navegador en 5 segundos...")
    time.sleep(5)
    driver.quit()
    print("Prueba finalizada.")