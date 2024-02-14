from typing import Annotated, Optional
from fastapi import FastAPI, File, UploadFile
from google.cloud import storage, documentai 
from google.api_core.client_options import ClientOptions
import os
from cc import process_document_sample
from test import descargar_imagen

app = FastAPI()
bucket_nombre = 'documentos-ocr-lucho'
objeto_nombre = 'img.jpeg'
destino_local = '/home/tomas071922/API-GCP-DNI-Extract/Img/img.jpeg'
@app.get("/")
def home():
    
    return {"message": "Hola Mundo"}

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    blob_name = "img.jpeg"
    bucket_name = "documentos-ocr-lucho"
    tipo = save_image(file, blob_name, bucket_name)

    # # # Descarga la imagen desde el bucket
    descargar_imagen(bucket_nombre, objeto_nombre, destino_local)
    a = process_document_sample(
    project_id="659531251163",
    location="us",
    processor_id="33b259122f65c043",
    file_path="/home/tomas071922/API-GCP-DNI-Extract/Img/img.jpeg",
    mime_type="image/jpeg"
    )
    return {"file_size": len(file)}


def save_image(file: bytes, blob_name: str, bucket_name: str):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        with blob.open("wb") as f:
            f.write(file)
            print("Guardado")
            tipo = type(f)
    except Exception as e:
        tipo = e
        print(e)
