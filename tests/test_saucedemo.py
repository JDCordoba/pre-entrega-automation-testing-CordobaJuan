import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importación de las funciones de ayuda (Page Objects / Helpers) creadas previamente
from utils.helpers import (
    URL,
    hacer_login,
    obtener_primer_producto,
    agregar_al_carrito,
    obtener_cantidad_carrito,
    is_element_present,
)

# TEST 1: AUTENTICACIÓN / LOGIN
def test_login_exitoso(driver):
    """
    Objetivo: Verificar que un usuario pueda iniciar sesión correctamente 
    utilizando credenciales válidas y sea redirigido a la pantalla principal.
    """
    # 1. Navega a la página de inicio de SauceDemo
    driver.get(URL)

    # 2. Espera explícita hasta que el input del usuario esté cargado en pantalla
    campo_usuario = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    # 3. Completa el formulario de login y hace clic en el botón de ingreso
    campo_usuario.send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # 4. Sincronización: Espera a que el navegador complete la redirección al inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )

    # 5. ASERSIONES
    # Verifica que la URL del navegador sea la correspondiente a la tienda interna
    assert "inventory.html" in driver.current_url, "ERROR: No se redirigió a la página de inventario."
    # Verifica que el título de la pestaña del navegador sea el correcto
    assert driver.title == "Swag Labs", f"ERROR: El título de la página cambio inesperadamente: {driver.title}"

    print("LOG: Login exitoso y validado. El usuario se encuentra en inventory.html")


# TEST 2: INTERFAZ Y CATÁLOGO DE PRODUCTOS
def test_verificacion_catalogo(driver):
    """
    Objetivo: Verificar que la tienda cargue correctamente su catálogo de productos
    y que los componentes esenciales de la interfaz de usuario estén visibles.
    """
    # 1. Realiza el inicio de sesión utilizando la función automatizada compartida
    hacer_login(driver)

    # 2. Valida que el título general de la página siga siendo el correcto
    assert driver.title == "Swag Labs", f"ERROR: Título de página incorrecto: {driver.title}"

    # 3. Espera a que los bloques de productos se rendericen completamente en el HTML
    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    # Valida que la lista de productos devuelta no venga vacía (debe haber stock en la tienda)
    assert len(productos) > 0, "ERROR: La lista de catálogo se encuentra vacía."
    print(f"LOG: Catálogo cargado. Se encontraron {len(productos)} productos en pantalla.")

    # 4. Extrae la información del primer producto visible mediante nuestro helper
    nombre, precio = obtener_primer_producto(driver)
    print(f"LOG: Datos del primer producto capturados -> Nombre: {nombre} | Precio: {precio}")

    # 5. ASERSIONES VISUALES: Comprueba la existencia de elementos clave en la botonera e interfaz
    assert is_element_present(driver, By.ID, "react-burger-menu-btn"), "ERROR: El menú lateral (Burger) no está visible."
    assert is_element_present(driver, By.CLASS_NAME, "product_sort_container"), "ERROR: El filtro de ordenamiento por precio/nombre no está visible."
    assert is_element_present(driver, By.CLASS_NAME, "shopping_cart_link"), "ERROR: El ícono del carrito de compras no está visible."

    print("LOG: Validación de catálogo completada con éxito. Interfaz OK.")


# TEST 3: FLUJO DE COMPRA / CARRITO
def test_funcionalidad_carrito(driver):
    """
    Objetivo: Validar el ciclo de vida básico del carrito de compras:
    Verificar estado vacío inicial -> Añadir producto -> Confirmar actualización de alertas -> Validar persistencia en checkout.
    """
    # 1. Inicia sesión en la plataforma
    hacer_login(driver)

    # 2. Validación de Estado Inicial: El carrito debe arrancar sin elementos (Badge oculto o en 0)
    cantidad_inicial = obtener_cantidad_carrito(driver)
    assert cantidad_inicial == 0, f"ERROR: El carrito no inició vacío. Cantidad actual: {cantidad_inicial}"

    # 3. Ejecuta la acción de agregar el primer ítem disponible y guarda su nombre para comparación cruzada
    nombre_producto = agregar_al_carrito(driver)
    print(f"LOG: Acción ejecutada -> Producto añadido: {nombre_producto}")

    # 4. Valida que el contador del carrito (badge rojo) se haya actualizado exactamente al valor 1
    cantidad = obtener_cantidad_carrito(driver)
    assert cantidad == 1, f"ERROR: El contador del carrito no se actualizó a 1. Cantidad real: {cantidad}"
    print("LOG: El contador visual del carrito se actualizó correctamente a '1'.")

    # 5. Navegación hacia el resumen: Hace clic sobre el ícono del carrito para abrir la lista
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    # 6. Sincroniza y espera a que el navegador ingrese a la sección del carrito de compras
    WebDriverWait(driver, 10).until(
        EC.url_contains("cart.html")
    )
    assert "cart.html" in driver.current_url, "ERROR: Falló el direccionamiento hacia la URL del carrito."

    # 7. Valida que la grilla del resumen contenga exactamente un solo producto listado
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 1, f"ERROR: Se esperaba 1 solo producto en el resumen, pero se encontraron: {len(items)}"

    # 8. Verificación de integridad de datos: Compara que el texto del producto en el carrito coincida con el que clickeamos antes
    nombre_en_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert nombre_en_carrito == nombre_producto, \
        f"ERROR: Discrepancia de datos en el carrito. Esperaba: '{nombre_producto}' pero se muestra: '{nombre_en_carrito}'"

    print(f"LOG: Test de flujo de carrito finalizado con éxito. El artículo '{nombre_en_carrito}' se encuentra guardado.")
