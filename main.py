from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
import openai
import uvicorn

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
    """Genera múltiples variaciones de prompts cinematográficos optimizados para Sora, Google Veo 2 y Runway con una estructura definida."""
    if "No image provided" in image_analysis:
        return ["Error: No image was uploaded. Please provide an image to generate cinematic prompts."]
    
    parts = image_analysis.split(". ")
    scene = parts[0] if len(parts) > 0 else "A cinematic landscape"
    subject = parts[1] if len(parts) > 1 else "A character in motion"
    lighting = parts[2] if len(parts) > 2 else "Soft, ambient lighting"
    aesthetics = parts[3] if len(parts) > 3 else "A blend of realism and surrealism"
    
    prompts = [
        f"[Camera movement]: A dynamic tracking shot follows the action. [Establishing scene]: {scene}. [Main subject]: {subject}. [Illumination]: {lighting}. [Aesthetics]: {aesthetics}.",
        f"[Camera movement]: A sweeping aerial view reveals the environment. [Establishing scene]: {scene}. [Main subject]: {subject}. [Illumination]: {lighting}. [Aesthetics]: {aesthetics}.",
        f"[Camera movement]: A slow-motion close-up intensifies the moment. [Establishing scene]: {scene}. [Main subject]: {subject}. [Illumination]: {lighting}. [Aesthetics]: {aesthetics}.",
    ]
    
    return prompts

@app.post("/generate_prompt/")
async def generate_prompt(file: UploadFile = File(...)):
    """Recibe una imagen, la analiza y genera prompts cinematográficos."""
    image_bytes = await file.read()
    image_analysis = analyze_image(image_bytes)
    prompts = generate_cinematic_prompts(image_analysis)
    return {"prompts": prompts}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
