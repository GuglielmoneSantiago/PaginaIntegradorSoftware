## Documentación para desarrolladores

### Prerrequisitos

- Python 3.12
- MongoDB (Compass o cualquier otro cliente MongoDB)

### Configuración del backend

1. En el directorio base del proyecto, crear entorno virtual de Python:
    ```
    python3.12 -m venv venv
    ```

2. Activar entorno creado:
    ```
    venv/Scripts/Activate.ps1
    ```
    - Quizás se deba cambiar la [directiva de ejecución](https://learn.microsoft.com/es-es/powershell/module/microsoft.powershell.security/set-executionpolicy) del sistema para poder ejecutar `Activate.ps1`. En este caso, desde un PowerShell como administrador, ejecutar:
        ```
        Set-ExecutionPolicy AllSigned
        ```

3. Instalar librerías requeridas:
    ```
    pip install -r requirements.txt
    ```


### Ejecución del proyecto

1. Activar el entorno virtual de Python (ver configuración de backend, paso 2).


2. Desde `backend/` (`cd backend/`), iniciar servidor local:
    ```
    uvicorn bck:app --reload
    ```

### URLs de interés
1. Página del formulario:

    `http://localhost:8000`

2. Página de agradecimiento una vez completado el cuestionario:

    `http://127.0.0.1:8000/finalEncuesta.html`

3. Página de resultados (muestra gráficos y un botón para descargar datos captados):

    `http://localhost:8000/ver_grafico`
