import os
from fastapi import FastAPI, Form, HTTPException, Request,Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import plotly.graph_objects as go
import uvicorn
import asyncio

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
    birth_year: Optional [int] = Form(...),
    gender: Optional [str] = Form(...),
    textura: Optional [str] = Form(...),
    consistencia: Optional [str] = Form(...),
    chocolate: Optional [str] = Form(...),
    atraccion: Optional [str] = Form(...),
    expectativa: Optional [str] = Form(...),
    humedad: Optional [str] = Form(...),
    sabores: Optional [str] = Form(...),
    respuesta7: str = Form(...)
):
    try:
        # Crear el documento a insertar en MongoDB
        document = {
            "birth_year": birth_year,
            "gender": gender,
            "textura": textura,
            "consistencia": consistencia,
            "chocolate": chocolate,
            "atraccion": atraccion,
            "expectativa": expectativa,
            "humedad": humedad,
            "sabores": sabores,
            "respuesta7": respuesta7
        }
        # Insertar el documento en MongoDB
        result=collection.insert_one(document)
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

@app.get("/graph")
async def get_graph():
    try:
        # Extraer datos de la base de datos para el gráfico
        cursor = collection.find({})
        satisfaction_levels = []
        for doc in cursor:
            if 'satisfaction_level' in doc:
                satisfaction_levels.append(doc["satisfaction_level"])
            else:
                # Manejo de documentos sin el campo 'satisfaction_level'
                # Puedes decidir ignorar estos documentos o realizar algún otro tipo de manejo
                pass

        # Crear el gráfico tipo telaraña
        categories = ['Muy insatisfecho', 'Insatisfecho', 'Neutral', 'Satisfecho', 'Muy satisfecho']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=satisfaction_levels,
            theta=categories,
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=False
        )

        graph_html = fig.to_html(full_html=False)
        return JSONResponse(content={"graph": graph_html}, media_type="application/json; charset=utf-8")
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
