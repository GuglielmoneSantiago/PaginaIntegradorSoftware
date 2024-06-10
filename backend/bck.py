import os
import tempfile
from fastapi import FastAPI, Form, HTTPException, Request,Response
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from matplotlib import pyplot as plt
from numpy import pi
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

import plotly.graph_objects as go
import uvicorn
import asyncio
from io import BytesIO
import base64

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["encuesta_db"]
# Verificar y crear la colección "responses" si no existe
if "encuestas" not in db.list_collection_names():
    db.create_collection("encuestas")

collection = db["encuestas"]

# Construir la ruta absoluta al directorio CSS
pagina_Resultado= os.path.join(os.path.dirname(__file__), '../src/HTML/paginarResultados.html')
directorio_css = os.path.join(os.path.dirname(__file__), '../src/CSS')
paginaEncuesta_html = os.path.join(os.path.dirname(__file__), '../src/HTML/paginaEncuesta.html')
html_directory_final = os.path.join(os.path.dirname(__file__), '../src/HTML/finalEncuesta.html')

# Montar el directorio estático
app.mount("/static", StaticFiles(directory=directorio_css), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open(paginaEncuesta_html, encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})

@app.post("/submit")
async def read_form(
    birth_year: Optional[int] = Form(...),
    gender: Optional[str] = Form(...),
    textura: Optional[str] = Form(...),
    consistencia: Optional[int] = Form(...),
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

#Pregunta 1
def obtener_datos_pregunta1():
    cursor = collection.find({})
    respuestas = {"Esponjoso": 0, "Crujiente": 0, "Blando": 0, "Duro": 0}
    for doc in cursor:
        if "textura" in doc:
            respuesta = doc["textura"]
            if respuesta in respuestas:
                respuestas[respuesta] += 1
    return respuestas

    
@app.get("/graph/pregunta1", response_class=JSONResponse)
async def get_graph_pregunta1():
    respuestas = obtener_datos_pregunta1()
    etiquetas = list(respuestas.keys())
    imagen_barras = generar_grafico_barras(respuestas,etiquetas)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_barras.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_barra_pregunta_uno = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_barra_pregunta_uno": imagen_base64_barra_pregunta_uno}

def generar_grafico_barras(respuestas,etiquetas):
    fig, ax = plt.subplots()
    ax.bar(etiquetas, respuestas.values())
    ax.set_xlabel('Respuestas')
    ax.set_ylabel('Cantidad')
    ax.set_title('Respuestas a la Pregunta 1')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
#termina pregunta 1 

#Comienza pregunta 2 
def obtener_datos_pregunta2():
    cursor = collection.find({})
    respuestas = {"Demasiado": 0, "Mucho": 0, "Poco": 0, "Nada": 0}
    for doc in cursor:
        if "consistencia" in doc:
            respuesta = doc["consistencia"]
            if respuesta in respuestas:
                respuestas[respuesta] += 1
    return respuestas

@app.get("/graph/pregunta2", response_class=JSONResponse)
async def get_graph_pregunta1():
    respuestas = obtener_datos_pregunta2()
    etiquetas = list(respuestas.keys())
    imagen_barras = generar_grafico_barras_dos(respuestas,etiquetas)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_barras.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_barra_pregunta_dos = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_barra_pregunta_dos": imagen_base64_barra_pregunta_dos}

def generar_grafico_barras_dos(respuestas,etiquetas):
    fig, ax = plt.subplots()
    ax.bar(etiquetas, respuestas.values())
    ax.set_xlabel('Respuestas')
    ax.set_ylabel('Cantidad')
    ax.set_title('Respuestas a la Pregunta 2')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
#Termina pregunta 2

#Pregunta 3 
def obtener_datos_chocolate():
    cursor = collection.find({})
    total_respuestas = 0
    respuestas_chocolate = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for doc in cursor:
        if "chocolate" in doc:
            total_respuestas += 1
            respuesta = doc["chocolate"]
            if respuesta in respuestas_chocolate:
                respuestas_chocolate[respuesta] += 1
    
    # Calcular los porcentajes
    porcentajes_chocolate = {str(key): (value / total_respuestas) * 100 for key, value in respuestas_chocolate.items()}
    
    return porcentajes_chocolate

def generar_grafico_torta_chocolate(porcentajes_chocolate):
    fig, ax = plt.subplots()
    ax.pie(porcentajes_chocolate.values(), labels=porcentajes_chocolate.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Valoración del Chocolate')
    return fig

@app.get("/graph/chocolate", response_class=JSONResponse)
async def get_graph_chocolate():
    porcentajes_chocolate = obtener_datos_chocolate()
    imagen_torta_chocolate = generar_grafico_torta_chocolate(porcentajes_chocolate)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_torta_chocolate.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_chocolate = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_chocolate": imagen_base64_chocolate}
#finaliza pregunta 3

#Pregunta 4 
def obtener_datos_atraccion():
    cursor = collection.find({})
    total_respuestas = 0
    respuestas_atraccion = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for doc in cursor:
        if "chocolate" in doc:
            total_respuestas += 1
            respuesta = doc["chocolate"]
            if respuesta in respuestas_atraccion:
                respuestas_atraccion[respuesta] += 1
    
    # Calcular los porcentajes
    porcentajes_atraccion = {str(key): (value / total_respuestas) * 100 for key, value in respuestas_atraccion.items()}
    
    return porcentajes_atraccion

def generar_grafico_torta_atraccion(porcentajes_atraccion):
    fig, ax = plt.subplots()
    ax.pie(porcentajes_atraccion.values(), labels=porcentajes_atraccion.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Valoración de la atraccion')
    return fig

@app.get("/graph/atraccion", response_class=JSONResponse)
async def get_graph_atraccion():
    porcentajes_atraccion = obtener_datos_atraccion()
    imagen_torta_atraccion = generar_grafico_torta_atraccion(porcentajes_atraccion)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_torta_atraccion.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_atraccion = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_atraccion": imagen_base64_atraccion}
#finaliza pregunta 4

#Pregunta 5 
def obtener_datos_expectativa():
    cursor = collection.find({})
    total_respuestas = 0
    respuestas_expectativa = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for doc in cursor:
        if "expectativa" in doc:
            total_respuestas += 1
            respuesta = doc["expectativa"]
            if respuesta in respuestas_expectativa:
                respuestas_expectativa[respuesta] += 1
    
    # Calcular los porcentajes
    porcentajes_expectativa = {str(key): (value / total_respuestas) * 100 for key, value in respuestas_expectativa.items()}
    
    return porcentajes_expectativa

def generar_grafico_torta_expectativa(porcentajes_expectativa):
    fig, ax = plt.subplots()
    ax.pie(porcentajes_expectativa.values(), labels=porcentajes_expectativa.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title('Valoración de las Expectativas')
    return fig

@app.get("/graph/expectativa", response_class=JSONResponse)
async def get_graph_expectativa():
    porcentajes_expectativa = obtener_datos_expectativa()
    imagen_torta_expectativa = generar_grafico_torta_expectativa(porcentajes_expectativa)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_torta_expectativa.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_expectativa = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_expectativa": imagen_base64_expectativa}
#finaliza pregunta 5

#Pregunta 7
def obtener_datos_pregunta7():
    cursor = collection.find({})
    respuestas = {"Dulce": 0, "Amargo": 0, "Salado": 0, "Acido": 0}
    for doc in cursor:
        if "sabores" in doc:
            respuesta = doc["sabores"]
            if respuesta in respuestas:
                respuestas[respuesta] += 1
    return respuestas

    
@app.get("/graph/sabores", response_class=JSONResponse)
async def get_graph_pregunta7():
    respuestas = obtener_datos_pregunta7()
    etiquetas = list(respuestas.keys())
    imagen_barras = generar_grafico_barras_sabores(respuestas,etiquetas)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_barras.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64_barra_pregunta_siete = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64_barra_pregunta_siete": imagen_base64_barra_pregunta_siete}

def generar_grafico_barras_sabores(respuestas,etiquetas):
    fig, ax = plt.subplots()
    ax.bar(etiquetas, respuestas.values())
    ax.set_xlabel('Respuestas')
    ax.set_ylabel('Cantidad')
    ax.set_title('Respuestas a la Pregunta 7')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
#Finaliza pregunta 7
@app.get("/ver_grafico", response_class=HTMLResponse)
async def get_form():
    with open(pagina_Resultado, encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
