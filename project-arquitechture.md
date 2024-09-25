/astrology-api
|-- app.py                  # Archivo principal de Flask, define la creación de la app y las rutas
|-- requirements.txt        # Dependencias del proyecto
|-- /astro                   # Módulo con la lógica de cálculo y manejo de datos
    |-- __init__.py          # Inicialización del módulo, posiblemente vacío
    |-- calculations.py      # Funciones de cálculo para las posiciones planetarias y las casas
    |-- constants.py         # Datos constantes, como los aspectos y los signos zodiacales
    |-- models.py            # Clases para manejar estructuras de datos complejas
    |-- utils.py             # Funciones utilitarias, como parsing de fechas
|-- /tests                   # Directorio para pruebas unitarias
    |-- __init__.py          # Inicialización del módulo de tests
    |-- test_calculations.py # Pruebas para las funciones de cálculo
|-- /instance                # Configuración específica del entorno que no se debe versionar
    |-- config.py            # Archivo de configuración para la instancia de Flask
