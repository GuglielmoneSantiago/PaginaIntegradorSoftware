import os
import tempfile
from fastapi import FastAPI, Form, HTTPException, Request,Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from matplotlib import pyplot as plt
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from grafico_telarania import generar_grafico_telarana
import plotly.graph_objects as go
import uvicorn
import asyncio
from io import BytesIO
import base64

app = FastAPI()

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["encuesta_db"]
# Verificar y crear la colección "responses" si no existe
if "encuestas" not in db.list_collection_names():
    db.create_collection("encuestas")

collection = db["encuestas"]

# Construir la ruta absoluta al directorio CSS
directorio_css = os.path.join(os.path.dirname(__file__), '../src/CSS')
prueba4_html = os.path.join(os.path.dirname(__file__), '../src/HTML/Prueba4.html')
html_directory_final = os.path.join(os.path.dirname(__file__), '../src/HTML/finalEncuesta.html')

# Montar el directorio estático
app.mount("/static", StaticFiles(directory=directorio_css), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open(prueba4_html, encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})

@app.post("/submit")
async def read_form(
    birth_year: Optional[int] = Form(...),
    gender: Optional[str] = Form(...),
    textura: Optional[str] = Form(...),
    consistencia: Optional[str] = Form(...),
    satisfactionRange: Optional[int] = Form(...),
    satisfactionRange_4: Optional[int] = Form(...),
    satisfactionRange_5: Optional[int] = Form(...),
    humedad: Optional[str] = Form(...),
    sabores: Optional[str] = Form(...),
    respuesta7: str = Form(...)
):
    try:
        # Crear el documento a insertar en MongoDB
        document = {
            "edad": birth_year,
            "genero": gender,
            "textura": textura,
            "consistencia": consistencia,
            "chocolate": satisfactionRange,
            "atraccion": satisfactionRange_4,
            "expectativa": satisfactionRange_5 ,
            "humedad": humedad,
            "sabores": sabores,
            "respuesta": respuesta7
        }
        # Insertar el documento en MongoDB
        result = collection.insert_one(document)
        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Error al insertar datos en MongoDB")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return Response(status_code=303, headers={"Location": "/finalEncuesta.html"})

@app.get("/finalEncuesta.html", response_class=HTMLResponse)
async def get_final_encuesta():
    with open(html_directory_final, encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)


def obtener_datos_encuestas():
    cursor = collection.find({})
    datos_encuestas = {
        'crujiente': 0,
        'blanda': 0,
        'dura': 0,
        'suave': 0,
        
    }
    for doc in cursor:
        if 'textura' in doc:
            textura = doc['textura']
            if textura in datos_encuestas:
                datos_encuestas[textura] += 1
    return datos_encuestas

@app.get("/graph")
async def get_graph():
    datos_encuestas = obtener_datos_encuestas()
    imagen_telarana = generar_grafico_telarana(datos_encuestas)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_telarana.savefig(tmpfile.name, format="png")

    # Leer el archivo temporal y convertirlo en una cadena base64
        with open(tmpfile.name, "rb") as image_file:
            imagen_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Construir el fragmento de HTML con la imagen base64
    html_content = f'<img src="data:image/png;base64,{imagen_base64}" alt="Grafico de Telarana">'
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
