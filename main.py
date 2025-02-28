from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import openai
import uvicorn
import multipart
import os
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")  # Asegúrate de definir tu clave API

app = FastAPI(
    title="Veo2 Plugin API",
    description="API para analizar imágenes y generar prompts cinematográficos.",
    version="1.0",
    servers=[
        {"url": "https://veo2-plugin.onrender.com", "description": "Servidor en Render"}
    ]
)

def analyze_image(image_bytes):
    """Convierte la imagen a base64 y la envía correctamente a OpenAI Vision API."""
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data = f"data:image/jpeg;base64,{image_base64}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are an AI that analyzes images and describes cinematic elements."},
            {"role": "user", "content": [
                {"type": "text", "text": "Describe the cinematic elements of this image, including setting, lighting, characters, and camera perspective."},
                {"type": "image_url", "image_url": image_data}
            ]}
        ],
        max_tokens=200
    )
    return response["choices"][0]["message"]["content"]

def generate_cinematic_prompts(image_analysis):
    """Genera múltiples variaciones de prompts cinematográficos basados en el análisis de la imagen."""
    prompts = [
        f"1. {image_analysis} The shot captures intensity and atmosphere with dynamic angles.",
        f"2. A cinematic depiction of {image_analysis}. The camera moves fluidly to enhance the storytelling.",
        f"3. {image_analysis} combined with expressive framing and lighting techniques, creating a dramatic effect."
    ]
    return prompts

@app.post("/generate_prompt/")
async def generate_prompt(file: UploadFile = File(...)):
    """Recibe una imagen, la convierte a base64, la analiza con OpenAI Vision y genera prompts cinematográficos."""
    image_bytes = await file.read()
    image_analysis = analyze_image(image_bytes)
    prompts = generate_cinematic_prompts(image_analysis)
    return {
        "image_analysis": image_analysis,
        "cinematic_prompts": prompts
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
