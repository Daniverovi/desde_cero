from fastapi import FastAPI, HTTPException
import os
from pydantic import BaseModel

app = FastAPI()

FILES_DIR = "./files"
os.makedirs(FILES_DIR, exist_ok=True)

class FileCreate(BaseModel):
    name: str
    content: str

@app.get("/")
async def root():
    return {"message": "Hello Worldddd"}

@app.get("/files/{file_name}")
def read_file(file_name: str):
    """Leer el contenido de un archivo."""
    file_path = os.path.join(FILES_DIR, file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"name": file_name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files")
def list_files():
    """Listar todos los archivos disponibles."""
    try:
        files = os.listdir("./files")
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/files")
def create_file(file: FileCreate):
    """Crear un nuevo archivo con contenido dado."""
    file_path = os.path.join(FILES_DIR, file.name)
    if os.path.exists(file_path):
        raise HTTPException(status_code=400, detail="El archivo ya existe")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file.content)
        return {"message": f"Archivo '{file.name}' creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))