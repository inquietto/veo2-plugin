from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import openai
import uvicorn
import multipart

app = FastAPI()

def analyze_image(image_bytes):
    """Simula el análisis de una imagen y extrae elementos clave."""
    # Aquí podrías integrar OpenAI Vision o CLIP para análisis avanzado
    return {
        "scene": "cyberpunk cityscape",
        "lighting": "neon reflections in the rain",
        "characters": "a lone bounty hunter walking with a cybernetic arm",
        "camera": "wide-angle tracking shot with dramatic lighting"
    }

def generate_cinematic_prompts(image_analysis):
    """Genera múltiples variaciones de prompts cinematográficos."""
    scene = image_analysis["scene"]
    lighting = image_analysis["lighting"]
    characters = image_analysis["characters"]
    camera = image_analysis["camera"]
    
    prompts = [
        f"1. A {scene}, illuminated by {lighting}. {characters} moves through the frame. The shot is a {camera}, capturing intensity and atmosphere.",
        f"2. In a futuristic {scene}, under {lighting}, {characters} takes center stage. The camera glides between dynamic angles for cinematic depth.",
        f"3. Drenched in {lighting}, the {scene} unfolds as {characters} moves in slow-motion. The shot transitions from close-ups to a sweeping drone perspective."
    ]
    return prompts

@app.post("/generate_prompt/")
async def generate_prompt(file: UploadFile = File(...)):
    """Recibe una imagen, la analiza y genera prompts cinematográficos."""
    image_bytes = await file.read()
    image_analysis = analyze_image(image_bytes)
    prompts = generate_cinematic_prompts(image_analysis)
    return {
        "image_analysis": image_analysis,
        "cinematic_prompts": prompts
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
