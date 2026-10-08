from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


# CONFIGURACIÓN Y DATOS DE PRUEBA (SauceDemo)
URL = "https://www.saucedemo.com/"
USUARIO = "standard_user"
CONTRASENA = "secret_sauce"


# FUNCIONES DE AYUDA Y NAVEGACIÓN

def is_element_present(driver, by, value, timeout=10):
    """
    Verifica de forma segura si un elemento existe en el DOM de la página.
    
    :param driver: Instancia del navegador de Selenium.
    :param by: El tipo de selector a usar (Ej: By.ID, By.CSS_SELECTOR).
    :param value: El valor del selector (Ej: "user-name").
    :param timeout: Tiempo máximo de espera en segundos antes de fallar.
    :return: True si el elemento aparece en el tiempo dado, False si expira la espera.
    """
    try:
        # Espera implícita/explícita hasta encontrar el elemento en el HTML
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        # Si se cumple el tiempo límite sin encontrarlo, evita que el script falle
        return False


def hacer_login(driver, usuario=USUARIO, contrasena=CONTRASENA):
    """
    Automatiza el proceso completo de inicio de sesión en SauceDemo.
    Asegura que el formulario esté cargado y que la redirección sea exitosa.
    """
    # 1. Abre la página web del sitio de pruebas
    driver.get(URL)

    # 2. Espera explícita hasta que el input de usuario sea visible en pantalla
    campo_usuario = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    # Escribe el nombre de usuario
    campo_usuario.send_keys(usuario)

    # 3. Busca los campos restantes y envía los datos (Contrasena y Click en ingresar)
    driver.find_element(By.ID, "password").send_keys(contrasena)
    driver.find_element(By.ID, "login-button").click()

    # 4. Espera de validación: Bloquea el script hasta confirmar que la URL cambió al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )


def obtener_primer_producto(driver):
    """
    Extrae los datos visibles del primer artículo que aparece en la tienda.
    
    :return: Una tupla con (nombre_del_producto, precio_del_producto).
    """
    # Recupera el texto de la etiqueta del nombre
    nombre = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    # Recupera el texto de la etiqueta del precio
    precio = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
    
    return nombre, precio


def agregar_al_carrito(driver):
    """
    Busca el primer artículo del catálogo, hace click en su botón 
    para añadirlo al carrito de compras y retorna su nombre.
    """
    # Llama a la función interna para capturar el nombre (e ignora el precio usando '_')
    nombre, _ = obtener_primer_producto(driver)

    # Localiza el primer botón de compra mediante una expresión XPath indexada [1]
    boton = driver.find_element(
        By.XPATH, "(//button[contains(@data-test, 'add-to-cart')])[1]"
    )
    boton.click()

    return nombre


def obtener_cantidad_carrito(driver):
    """
    Revisa el ícono del carrito en la esquina superior derecha 
    para saber cuántos productos hay listados actualmente.
    
    :return: El número entero de productos en el carrito. Si está vacío, retorna 0.
    """
    try:
        # Espera un máximo de 3 segundos a que aparezca el círculo rojo indicador (badge)
        badge = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        # Convierte el texto numérico del elemento web a un número entero de Python
        return int(badge.text)
    except TimeoutException:
        # Si el "badge" no aparece, significa que el carrito no posee ningún producto (0)
        return 0
