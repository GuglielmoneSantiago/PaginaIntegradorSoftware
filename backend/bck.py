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
    categorias = ['chocolate', 'atraccion', 'expectativa']
    datos_encuestas = {categoria: [] for categoria in categorias}

    for doc in cursor:
        for categoria in categorias:
            if categoria in doc:
                datos_encuestas[categoria].append(doc[categoria])

    return categorias, datos_encuestas

def generar_grafico_telarana(categorias, valores):
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))
    
    # Calcular los valores promedio y agregar el primer valor al final para cerrar el gráfico
    valores_promedio = [sum(valores[i]) / len(valores[i]) if len(valores[i]) > 0 else 0 for i in range(len(categorias))]
    valores_promedio.append(valores_promedio[0])  # Cerrar el gráfico
    
    # Ajustar los ángulos de las categorías
    angulos = [n / float(len(categorias)) * 2 * pi for n in range(len(categorias))]
    angulos.append(angulos[0])

    ax.fill(angulos, valores_promedio, alpha=0.25, color='b')
    ax.plot(angulos, valores_promedio, color='b')

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    ax.set_thetagrids([i * (360 / len(categorias)) for i in range(len(categorias))], categorias)
    ax.set_ylim(0, 5)

    ax.set_title('Telaraña de Resultados de la Encuesta', size=20, color='black', y=1.1,pad=1)
    
    return fig

 
@app.get("/graph", response_class=JSONResponse)
async def get_graph():
    categorias, datos_encuestas = obtener_datos_encuestas()
    valores = [datos_encuestas[categoria] for categoria in categorias]

    imagen_telarana = generar_grafico_telarana(categorias, valores)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_telarana.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    return {"imagen_base64": imagen_base64}

@app.get("/graph/view", response_class=HTMLResponse)
async def view_graph():
    categorias, datos_encuestas = obtener_datos_encuestas()
    valores = [datos_encuestas[categoria] for categoria in categorias]

    imagen_telarana = generar_grafico_telarana(categorias, valores)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
        imagen_telarana.savefig(tmpfile.name, format="png")

    with open(tmpfile.name, "rb") as image_file:
        imagen_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Construir la respuesta HTML con la imagen y la redirección
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="5; url=http://127.0.0.1:5500/src/HTML/paginarResultados.html">
        <title>Redirecting...</title>
    </head>
    <body>
        <img src="data:image/png;base64,{imagen_base64}" alt="Grafico de Telaraña">
    </body>
    </html>
    '''

    return HTMLResponse(content=html_content, headers={"Content-Type": "text/html; charset=utf-8"})

@app.get("/ver_grafico", response_class=HTMLResponse)
async def get_form():
    with open(pagina_Resultado, encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
