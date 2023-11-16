from fastapi import FastAPI
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hola Mundo"}


def save_image(file: bytes, folder_path: str):
    with open(os.path.join(folder_path,"image.jpg"), "wb") as f:
        f.write(file)

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    folder_path = "./Img"
    save_image(file, folder_path, file.filename)
    return {"file_size": len(file)}
