from fastapi import FastAPI
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from google.cloud import storage 
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hola Mundo"}


def save_image(file: bytes, blob_name: str, bucket_name: str):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        with blob.open("wb") as f:
            f.write(file)
            print("Guardado")
    except Exception as e:
        print(e)
    #with open(os.path.join(folder_path,"image.jpg"), "wb") as f:
    

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    blob_name = "img.jpeg"
    bucket_name = "documentos-ocr-lucho"
    save_image(file, blob_name, bucket_name)
    return {"file_size": len(file)}
