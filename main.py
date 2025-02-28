from fastapi import FastAPI, File, UploadFile, HTTPException
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
    """Convierte la imagen a base64 y la envía correctamente a OpenAI Vision API con un prompt mejorado."""
    if not image_bytes:
        return "No image provided. Unable to generate analysis."
    
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_data = f"data:image/jpeg;base64,{image_base64}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are an AI specializing in cinematic analysis. Describe the composition, lighting, atmosphere, and visual storytelling of this image in a detailed and artistic way. Do not identify people, but focus on the scene's aesthetics, color grading, and mood."},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this image as if it were a film scene. Describe its setting, lighting, color palette, framing, and the overall cinematic feeling. Provide a visually immersive description suitable for a movie prompt for AI video models like Sora, Google Veo 2, or Runway."},
                {"type": "image_url", "image_url": image_data}
            ]}
        ],
        max_tokens=300
    )
    return response["choices"][0]["message"]["content"]

def generate_cinematic_prompts(image_analysis):
    """Genera múltiples variaciones de prompts cinematográficos optimizados para Sora, Google Veo 2 y Runway."""
    if "No image provided" in image_analysis:
        return ["Error: No image was uploaded. Please provide an image to generate cinematic prompts."]
    
    prompts = [
        f"A cinematic scene: {image_analysis}. Designed for AI video generation, capturing intensity and atmosphere with dynamic angles.",
        f"This frame evokes {image_analysis}, optimized for Sora, Google Veo 2, and Runway. The camera moves fluidly to enhance storytelling.",
        f"{image_analysis}, combined with expressive framing and lighting techniques, creating a dramatic and visually striking effect suitable for high-quality AI-generated videos."
    ]
    return prompts

@app.post("/generate_prompt/")
async def generate_prompt(file: UploadFile = File(None)):
    """Recibe una imagen, la convierte a base64, la analiza con OpenAI Vision y genera prompts cinematográficos optimizados para IA de video."""
    if file is None:
        raise HTTPException(status_code=400, detail="No image file uploaded. Please upload an image.")
    
    image_bytes = await file.read()
    image_analysis = analyze_image(image_bytes)
    prompts = generate_cinematic_prompts(image_analysis)
    return {
        "image_analysis": image_analysis,
        "cinematic_prompts": prompts
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
