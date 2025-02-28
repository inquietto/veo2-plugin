from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI(
    title="Veo2 Plugin API",
    description="API para analizar imágenes y generar prompts cinematográficos.",
    version="1.0",
    servers=[
        {"url": "https://veo2-plugin.onrender.com", "description": "Servidor en Render"}
    ]
)

@app.get("/openapi.json")
async def get_openapi_json():
    """Sirve manualmente el archivo openapi.json para que ChatGPT lo detecte."""
    return JSONResponse(content=get_openapi(title=app.title, version=app.version, openapi_version="3.0.3", routes=app.routes))

@app.get("/ai-plugin.json")
async def get_ai_plugin():
    """Sirve el archivo ai-plugin.json para que ChatGPT pueda leerlo."""
    return FileResponse("ai-plugin.json")
