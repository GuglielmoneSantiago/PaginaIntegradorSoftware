from fastapi import FastAPI, Form, HTTPException, Request,Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
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

# Montar los archivos estáticos (CSS)
app.mount("/src/CSS", StaticFiles(directory="../src/CSS"), name="static")



@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open("../src/paginaEncuesta.html", encoding="utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content, headers={"Content-Type": "text/html; charset=utf-8"})


@app.post("/submit")
async def read_form(
    name: str = Form(...),
    email: str = Form(...),
    age: int = Form(...),
    role: str = Form(...),
    programming: str = Form(...),
    best_language: str = Form(...),
    interest: List[str] = Form(...),
    satisfactionRange: int = Form(...),
    comments: Optional[str] = Form(None)
):
    try:
        # Crear el documento a insertar en MongoDB
        document = {
            "name": name,
            "email": email,
            "age": age,
            "role": role,
            "programming": programming,
            "best_language": best_language,
            "interest": interest,
            "satisfactionRange": satisfactionRange,
            "comments": comments
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
    with open("../src/finalEncuesta.html", encoding="utf-8") as f:
        content = f.read()
        
    return HTMLResponse(content=content)

@app.get("/graph", response_class=HTMLResponse)
async def get_graph():
    try:
        # Extraer datos de la base de datos para el gráfico
        cursor = collection.find({})
        satisfaction_levels = [doc["satisfaction_level"] for doc in cursor]
        # Crear el gráfico tipo telaraña
        # Aquí, debes implementar la lógica para crear el gráfico con Plotly y devolverlo como HTML
        # Este es un ejemplo simple que necesitas adaptar
        import plotly.graph_objects as go

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
        return HTMLResponse(content=graph_html)
    except asyncio.CancelledError:
        return {"message": "La tarea fue cancelada"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
