from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import requests
import openai
import uvicorn
import os
import base64
import json
from PIL import Image
import io

# Configuración de la API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Asegúrate de definir tu clave API en Render

# Crear la instancia de FastAPI
app = FastAPI(
    title="Veo2 Plugin API",
    description="API para analizar imágenes y generar prompts cinematográficos.",
    version="1.0",
    servers=[
        {"url": "https://veo2-plugin.onrender.com", "description": "Servidor en Render"}
    ]
)

class ImageRequest(BaseModel):
    image_url: str = None

def analyze_image(image_bytes):
    """Convierte la imagen a base64 y la envía correctamente a OpenAI Vision API con un prompt mejorado."""
    if not image_bytes:
        return "No image provided. Unable to generate analysis."
    
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data = f"data:image/jpeg;base64,{image_base64}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are an AI specializing in cinematic analysis. Describe the composition, lighting, atmosphere, and visual storytelling of this image in a detailed and artistic way. Do not identify people, but focus on the scene's aesthetics, color grading, and mood."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this image as if it were a film scene. Describe its setting, lighting, color palette, framing, and the overall cinematic feeling."},
                    {"type": "image_url", "image_url": image_data}
                ]}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error in OpenAI API: {str(e)}"

def generate_cinematic_prompts(image_analysis):
    """Genera múltiples variaciones de prompts cinematográficos."""
    try:
        analysis_json = json.loads(image_analysis) if isinstance(image_analysis, str) else image_analysis
        scene = analysis_json.get("scene", "a mysterious location")
        lighting = analysis_json.get("lighting", "dramatic lighting")
        characters = analysis_json.get("characters", "a lone protagonist")
        camera = analysis_json.get("camera", "wide-angle shot")
        
        prompts = [
            f"A {scene}, illuminated by {lighting}. {characters} moves through the frame. The shot is a {camera}, capturing intensity and atmosphere.",
            f"In a futuristic {scene}, under {lighting}, {characters} takes center stage. The camera glides between dynamic angles for cinematic depth.",
            f"Drenched in {lighting}, the {scene} unfolds as {characters} moves in slow-motion. The shot transitions from close-ups to a sweeping drone perspective."
        ]
        return prompts
    except Exception as e:
        return [f"Error generating prompts: {str(e)}"]

@app.post("/generate_prompt/")
async def generate_prompt(file: UploadFile = File(None), image_url: str = Form(None)):
    """Recibe una imagen, ya sea un archivo o una URL, la convierte a base64, la analiza con OpenAI Vision y genera prompts cinematográficos."""
    image_bytes = None

    # Si el usuario sube un archivo
    if file:
        image_bytes = await file.read()
    # Si el usuario envía una URL de imagen
    elif image_url:
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_bytes = response.content
            else:
                raise HTTPException(status_code=400, detail="Failed to download image from URL.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error fetching image: {str(e)}")

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No valid image provided.")

    # Analizar la imagen con OpenAI Vision
    image_analysis = analyze_image(image_bytes)
    prompts = generate_cinematic_prompts(image_analysis)

    return {
        "image_analysis": image_analysis,
        "cinematic_prompts": prompts
    }

@app.get("/openapi.json")
async def get_openapi_json():
    """Sirve manualmente el archivo openapi.json para que ChatGPT lo detecte correctamente."""
    return JSONResponse(content=app.openapi())

@app.get("/ai-plugin.json")
async def get_ai_plugin():
    """Sirve el archivo ai-plugin.json para que ChatGPT pueda leerlo."""
    return FileResponse("ai-plugin.json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
