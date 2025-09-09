Este script es una excelente demostración de una prueba E2E (End-to-End o de Extremo a Extremo), que simula un recorrido completo de un usuario a través de varias funcionalidades de la aplicación.

1. Importaciones: Las Herramientas que Usaremos 🧰
Python

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
Cada línea import trae una herramienta específica a nuestro "taller" de programación.

webdriver: Es el corazón de Selenium. Es lo que nos permite dar órdenes a un navegador (Chrome, Firefox, etc.) desde nuestro código.

Service: Es un objeto auxiliar que se encarga de iniciar y detener el chromedriver.exe, el "traductor" entre nuestro script y el navegador Chrome.

By: Es un ayudante para localizar elementos. Nos provee las diferentes estrategias de búsqueda, como By.ID, By.NAME, By.LINK_TEXT, etc.

WebDriverWait: Esta es la herramienta para las esperas inteligentes o explícitas. Le dice al script que espere un tiempo máximo hasta que ocurra una condición específica, en lugar de usar pausas fijas.

expected_conditions as EC: Son las "condiciones" que WebDriverWait utiliza. Le damos un alias as EC para que sea más corto y fácil de escribir. Ejemplos son EC.element_to_be_clickable (esperar a que un elemento se pueda cliquear) o EC.visibility_of_element_located (esperar a que un elemento sea visible).

time: Una librería básica de Python que nos permite, entre otras cosas, usar time.sleep() para crear pausas fijas. En tu script, las usas principalmente para que puedas ver visualmente lo que está pasando, lo cual es útil durante el desarrollo.

2. Configuración Maestra: Preparando el Terreno 🚗
Python

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15) 
driver.maximize_window()
Aquí preparamos todo antes de que empiecen las pruebas. Esto se hace una sola vez.

service = Service(...): Creamos el servicio que manejará nuestro chromedriver.exe.

driver = webdriver.Chrome(...): ¡Esta es la línea clave! Aquí se abre la ventana del navegador Chrome que será controlada por nuestro script. El objeto driver es nuestro "control remoto" para el navegador. Todas las órdenes (get, find_element, click) se las daremos a driver.

wait = WebDriverWait(driver, 15): Creamos nuestro objeto de espera inteligente. A partir de ahora, cada vez que usemos wait.until(...), el script esperará un máximo de 15 segundos a que la condición se cumpla. Si no se cumple en ese tiempo, la prueba fallará con un error (TimeoutException), lo cual es bueno porque nos dice que algo en la página no cargó a tiempo.

driver.maximize_window(): Simplemente maximiza la ventana del navegador para asegurar que todos los elementos sean visibles.

3. El Bloque try...finally: La Red de Seguridad 🥅
Python

try:
    # ... todo el código de las pruebas ...
finally:
    # ... código para cerrar el navegador ...
Esta es una estructura fundamental en programación para asegurar que ciertas acciones se realicen sin importar lo que pase.

try: El script intentará ejecutar todo el código que está dentro de este bloque.

finally: Este bloque se ejecutará siempre al final, sin importar si el código en el try funcionó a la perfección o si falló por un error.

¿Por qué es crucial? Si una de tus pruebas falla a la mitad (por ejemplo, no encuentra un botón), el script se detendría. Sin un finally, la ventana del navegador se quedaría abierta. El bloque finally garantiza que driver.quit() se llame siempre, cerrando el navegador y terminando el proceso limpiamente.

4. Flujo 1: Prueba de Login Fallido
Este flujo prueba un "caso negativo", es decir, que la aplicación reacciona correctamente a datos incorrectos.

Python

# 1.2. Clic para ir a HiMed Web (abre una nueva pestaña)
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Ingresar a HiMed Web"))).click()
wait.until(EC.number_of_windows_to_be(2))
driver.switch_to.window(driver.window_handles[1])
wait.until(EC.element_to_be_clickable(...)): Esta es la forma correcta de interactuar. El script espera hasta 15 segundos a que el enlace "Ingresar a HiMed Web" sea visible y esté habilitado para recibir un clic. Solo entonces...

.click(): ...hace clic en él.

wait.until(EC.number_of_windows_to_be(2)): Espera inteligentemente a que el número total de pestañas sea 2, confirmando que la nueva pestaña se abrió.

driver.switch_to.window(driver.window_handles[1]): Esta es la parte de manejo de pestañas. driver.window_handles es una lista de las pestañas abiertas. [0] es la original y [1] es la nueva. Con switch_to.window(), le decimos a nuestro "control remoto" (driver) que a partir de ahora todas las órdenes deben ejecutarse en esa nueva pestaña.

Python

# 1.3. Rellenamos el formulario de login con datos inválidos
wait.until(EC.element_to_be_clickable((By.ID, "nit_cc"))).send_keys("123456789")
driver.find_element(By.ID, "idV").send_keys("usuario_invalido")
# ... etc ...
find_element(By.ID, "nit_cc"): Busca un elemento en la página que tenga el atributo id="nit_cc". Usar ID es la estrategia más rápida y segura.

.send_keys("..."): Una vez encontrado el elemento (un campo de texto), esta acción simula a una persona escribiendo el texto proporcionado.

Python

# 1.5. Limpieza: Cerramos la pestaña de login y volvemos a la pestaña principal
driver.close()
driver.switch_to.window(driver.window_handles[0])
driver.close(): Cierra la pestaña actual en la que driver tiene el foco (en este caso, la de login).

driver.switch_to.window(driver.window_handles[0]): Devuelve el foco a la pestaña original para que el script pueda continuar desde allí.

5. Flujo 2: Prueba de Compra y Cancelación
Este flujo prueba un "caso positivo" completo, desde la selección de un producto hasta su eliminación.

Python

# Forzamos la recarga de la página para asegurar un estado limpio
driver.get("https://medsas.co/modulo-de-rips/")
driver.get("..."): Este comando le ordena al navegador navegar a una URL específica. Lo usas aquí para asegurar que el segundo flujo comience desde un punto de partida limpio y conocido.

Python

# 2.2. Cambiamos la cantidad a 7...
campo_cantidad = wait.until(EC.visibility_of_element_located((By.NAME, "quantity")))
campo_cantidad.clear()
campo_cantidad.send_keys("7")
EC.visibility_of_element_located: A diferencia de element_to_be_clickable, esta condición solo espera a que el elemento sea visible en la página, no necesariamente interactivo. Es útil para campos que pueden tardar en aparecer.

.clear(): Borra cualquier texto que ya exista en un campo de entrada. Es una buena práctica usarlo antes de un .send_keys() para asegurar que no se añada texto no deseado.

Python

# 2.5. Verificamos que la URL actual sea la de la página de inicio
wait.until(EC.url_to_be("https://medsas.co/"))
assert driver.current_url == "https://medsas.co/"
assert: Esta es la palabra clave para las verificaciones. assert comprueba si una condición es verdadera. Si driver.current_url (la URL actual) es igual a la esperada, el script continúa. Si no lo es, la prueba se detiene y falla, informándote que la aplicación no se comportó como se esperaba. Una prueba sin assert no es una prueba, es solo un script que ejecuta pasos.

Resumen Clave para una Entrevista
Si te preguntan por este código, aquí tienes los puntos clave que debes explicar:

Estructura Robusta: "El script está dentro de un bloque try...finally para garantizar que el navegador siempre se cierre, incluso si hay errores."

Esperas Explícitas: "No uso pausas fijas (time.sleep) para la lógica de la prueba. En su lugar, utilizo WebDriverWait con expected_conditions para sincronizar el script con el estado de la aplicación. Esto hace las pruebas más rápidas y fiables."

Manejo de Pestañas: "El script maneja múltiples pestañas del navegador, cambiando el foco entre ellas usando driver.switch_to.window y la lista de driver.window_handles."

Verificaciones (Assertions): "Al final de los flujos clave, utilizo assert para verificar que el estado de la aplicación (como la URL final) es el esperado. Esto es lo que determina si una prueba pasa o falla."

Pruebas E2E: "Este no es solo un script que prueba un botón. Es una suite de pruebas de extremo a extremo que simula un viaje de usuario completo, combinando un caso de prueba negativo (login fallido) con uno positivo (flujo de compra), lo que da una cobertura mucho más realista de la aplicación."




https://www.python.org/downloads/
pip install selenium
https://googlechromelabs.github.io/chrome-for-testing/




Pasos Clave para Aprender Postman
Entender las Peticiones HTTP:

GET: Para obtener datos (ej. traer la lista de citas de un paciente).

POST: Para crear nuevos datos (ej. registrar un nuevo usuario).

PUT/PATCH: Para actualizar datos existentes (ej. cambiar la hora de una cita).

DELETE: Para borrar datos (ej. cancelar una cita).

Crear tu Primera Petición:

Abre Postman, introduce la URL del "endpoint" de la API (te la tendrán que proporcionar los desarrolladores, ej. https://api.empresa.com/pacientes/123).

Selecciona el método correcto (GET, POST, etc.).

Si es necesario (para POST/PUT), ve a la pestaña "Body", selecciona "raw" y "JSON", y escribe los datos que quieres enviar.

Haz clic en "Send" y observa la respuesta.

Analizar la Respuesta:

Status Code: Es un número que indica el resultado. Los más importantes:

200 OK: Todo salió bien.

201 Created: Se creó un nuevo recurso con éxito.

400 Bad Request: Enviaste algo mal en tu petición.

401 Unauthorized: No tienes permiso (te falta un token de autenticación).

404 Not Found: El recurso que buscas no existe.

500 Internal Server Error: Hubo un error en el servidor.

Body: Son los datos que te devuelve el servidor, usualmente en formato JSON.

Colecciones y Entornos:

Colecciones: Agrupa tus peticiones de forma lógica (ej. una colección para "Gestión de Pacientes", otra para "Gestión de Citas").

Entornos: Te permite gestionar variables. Por ejemplo, puedes tener un entorno para "Pruebas" y otro para "Producción". En cada uno, defines una variable base_url (https://test.api.com y https://api.com). Así, puedes ejecutar la misma colección en diferentes entornos sin cambiar las URLs a mano.

Automatización con Scripts: Aquí es donde Postman brilla.

Tests: En la pestaña "Tests" de una petición, puedes escribir pequeños scripts en JavaScript para verificar la respuesta.

pm.test("La respuesta es 200 OK", function () { pm.response.to.have.status(200); });

pm.test("El nombre del paciente es correcto", function () { var jsonData = pm.response.json(); pm.expect(jsonData.nombre).to.eql("Carlos"); });

Pre-request Scripts: Scripts que se ejecutan antes de enviar la petición. Útil para, por ejemplo, generar un token de autenticación.




Paso 1: Cómo Encontrar el "Localizador" en 'Inspeccionar'
Antes de poder hacer clic o escribir, necesitas darle a Selenium la dirección exacta del elemento. A esta dirección la llamamos localizador. Piensa en ello como si le dieras a un GPS una dirección para encontrar una casa.

Para tu botón de ejemplo, así es como encuentras las posibles "direcciones" al inspeccionarlo:
<a class="button btn-himed button_size_1" href="https://m.medsas.co/" ...><span ...>Ingresar a HiMed Web</span></a>

Aquí tienes varias opciones de localizadores, de la más fácil a la más técnica:

Por el Texto Visible (la más fácil y recomendada para este caso) 📍:

Qué ves en la página: El texto "Ingresar a HiMed Web".

Estrategia en Selenium: By.LINK_TEXT (porque es un enlace <a>).

Valor a usar: "Ingresar a HiMed Web"

Por su Clase (Class):

Qué ves en el código: class="button btn-himed button_size_1"

Estrategia en Selenium: By.CLASS_NAME o, mejor aún, By.CSS_SELECTOR.

Valor a usar: Con By.CLASS_NAME puedes usar "btn-himed". Con By.CSS_SELECTOR puedes ser más específico escribiendo ".btn-himed".

Por otro Atributo (como href):

Qué ves en el código: href="https://m.medsas.co/"

Estrategia en Selenium: By.CSS_SELECTOR.

Valor a usar: a[href="https://m.medsas.co/"] (Esto se lee como: "busca un enlace a que tenga un atributo href con este valor exacto").

Recomendación para tu botón: La forma más clara y robusta es usar el texto visible. Es fácil de leer y es menos probable que cambie.

Paso 2: Cómo Escribir el Código para las Acciones
Una vez que has elegido tu localizador, escribir el código es muy sencillo. Siempre sigue dos pasos: 1. Encuentra el elemento (y espéralo) y 2. Realiza la acción.

Clic Sencillo 🖱️
Esta es la acción más común. Usando tu botón como ejemplo con el localizador By.LINK_TEXT.

Python

# Importa las herramientas necesarias al inicio de tu script
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dentro de tu código de prueba (asumiendo que ya tienes 'driver' y 'wait' configurados)

# 1. Espera inteligentemente a que el botón sea clickeable y guárdalo en una variable
boton_ingresar = wait.until(
    EC.element_to_be_clickable( (By.LINK_TEXT, "Ingresar a HiMed Web") )
)

# 2. Realiza la acción de hacer clic
boton_ingresar.click()
wait.until(...): Le dice a Selenium que espere hasta 15 segundos (o lo que hayas configurado) a que el botón no solo esté visible, sino también listo para ser presionado. Esto evita errores en páginas lentas.

.click(): Simula el clic de un mouse.

Escribir Texto ⌨️
Para escribir, primero buscas un campo de texto (<input> o <textarea>) y luego usas .send_keys().

Ejemplo: Imagina que en el inspector encuentras un campo de email: <input type="text" id="correo_usuario">

Python

# 1. Espera a que el campo de texto sea visible y guárdalo en una variable
campo_email = wait.until(
    EC.visibility_of_element_located( (By.ID, "correo_usuario") )
)

# 2. Es buena práctica borrar primero cualquier texto que pueda haber
campo_email.clear()

# 3. Escribe el texto deseado
campo_email.send_keys("un.correo.de.prueba@test.com")
.clear(): Borra el contenido del campo.

.send_keys(): Simula a una persona escribiendo en el teclado.

Doble Clic ⚡
El doble clic es una acción más avanzada y requiere una herramienta especial llamada ActionChains. Piensa en ActionChains como una forma de crear una secuencia de acciones complejas (como mover el mouse, arrastrar y soltar, o hacer doble clic).

Ejemplo: Imagina un botón que necesita un doble clic: <div id="boton_doble_clic">Haz doble clic aquí</div>

Python

# Importa la herramienta ActionChains al inicio de tu script
from selenium.webdriver.common.action_chains import ActionChains

# Dentro de tu código de prueba

# 1. Primero, encuentra el elemento como siempre
elemento_especial = wait.until(
    EC.element_to_be_clickable( (By.ID, "boton_doble_clic") )
)

# 2. Crea un objeto ActionChains
acciones = ActionChains(driver)

# 3. Define la secuencia de acciones (en este caso, solo un doble clic)
acciones.double_click(elemento_especial)

# 4. ¡MUY IMPORTANTE! Ejecuta las acciones definidas
acciones.perform()
ActionChains(driver): Inicializa el constructor de acciones.

.double_click(elemento): Le dices a la secuencia qué acción realizar y sobre qué elemento.

.perform(): Esta es la línea clave. Sin ella, las acciones solo se definen pero nunca se ejecutan.
