![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pytest](https://img.shields.io/badge/Pytest-9.x-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A)
![Firefox](https://img.shields.io/badge/Browser-Firefox-orange)
![Estado](https://img.shields.io/badge/Tests-3%20passed-brightgreen)

Proyecto de automatización de pruebas para saucedemo.com hecho para la pre-entrega del curso de Testing.

---

## Para qué sirve este proyecto

El objetivo es automatizar algunos flujos básicos del sitio saucedemo.com usando Selenium y Python. Los casos que probé son:

- login con usuario y contraseña válidos
- Que el catálogo de productos cargue bien
- Agregar un producto al carrito y verificar que esté ahí

---

## Tecnologías que use

- Python 3.10+
- Pytest
- Selenium WebDriver
- pytest-html (para el reporte)
- Firefox + GeckoDriver

---

## Cómo está organizado el proyecto

```
pre-entrega-automation-testing-CordobaJuan/
├── conftest.py           # configuración del driver y captura de screenshots en fallos
├── tests/
│   └── test_saucedemo.py # acá están los 3 tests
├── utils/
│   └── helpers.py        # funciones que reutilizo en los tests
├── reports/              # el reporte html se guarda acá
├── screenshots/          # las capturas en caso de fallo se guardan acá
└── README.md
```

---

## Cómo instalar las dependencias

1. Clonar el repo:

```bash
git clone https://github.com/JDCordoba/pre-entrega-automation-testing-CordobaJuan.git
cd pre-entrega-automation-testing-CordobaJuan
```

2. Instalar las librerías:

```bash
pip install selenium pytest pytest-html
```

3. Instalar GeckoDriver para Firefox:

Descargarlo desde https://github.com/mozilla/geckodriver/releases y asegurarse de que esté en el PATH.

---

## Cómo correr los tests

Solo los tests:

```bash
pytest tests/test_saucedemo.py -v
```

Con reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

---

## Tests incluidos

| Test | Qué verifica |
|---|---|
| test_login_exitoso | que con credenciales válidas redirija a inventory.html |
| test_verificacion_catalogo | que haya productos, título correcto y elementos de la interfaz |
| test_funcionalidad_carrito | agregar un producto y que aparezca bien en el carrito |

---

## Capturas automáticas

Si un test falla, se guarda automáticamente una captura en la carpeta `screenshots/` con el nombre del test y la fecha.

---

## Autor

Cordoba Juan - Curso de Automatización de Testing - Talento Tech
