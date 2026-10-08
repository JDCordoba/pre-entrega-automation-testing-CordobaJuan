import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
#from webdriver_manager.firefox import GeckoDriverManager



# Creo las carpetas que voy a necesitar si todavia no existen
def pytest_configure(config):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    if not os.path.exists("reports"):
        os.makedirs("reports")


# Este hook se ejecuta despues de cada test
# Si el test fallo, saca una captura de pantalla
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"failure_{item.name}_{timestamp}.png"
            driver.save_screenshot(f"screenshots/{nombre_archivo}")
            print(f"\nse guardo captura: {nombre_archivo}")


# Esta funcion abre firefox antes de cada test y lo cierra al terminar
@pytest.fixture (scope="module")
def driver():
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless") # descomentar para correr sin abrir el navegador

    # Selenium Manager se encarga de todo de forma nativa
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    yield driver

    driver.quit()