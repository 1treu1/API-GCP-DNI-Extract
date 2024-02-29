import os
from cc import process_document_sample
from typing import Annotated, Optional
from google.cloud import storage, documentai 
from fastapi import FastAPI, File, UploadFile
from google.api_core.client_options import ClientOptions

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hola Mundo"}

@app.post("/docs")
async def ClassifierDocs(file: Annotated[bytes, File()]):
    blob_name = "doc.pdf"
    bucket_name = "bk-upload-documents-ocr-api"
    SaveImage(file, blob_name, bucket_name)
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    classifier_id = "710060bd3e31a91d"
    result = Model(classifier_id,blob)

    if result[0].confidence >= 0.85:
        o = CamaraDeComercioOcr(blob_name,bucket_name)
        return o
    if result[1].confidence >= 0.85:
        o = CcOcr(blob_name,bucket_name)
        return o

    if result[2].confidence >= 0.85:
        o = RutOcr(blob_name,bucket_name)
        return o
    return None 

def SaveImage(file: bytes, blob_name: str, bucket_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with blob.open("wb") as f:
        f.write(file)
        print("Guardado")

def Model(processor_id, blob):
    try:
        result = process_document_sample(blob,
        project_id="934514998556",
        location="us",
        processor_id=processor_id,
        file_path=blob,
        mime_type= "application/pdf"
    )
    except:
        result = process_document_sample(blob,
        project_id="934514998556",
        location="us",
        processor_id=processor_id,
        file_path=blob,
        mime_type= "image/jpeg"
    )
    return result

def CamaraDeComercioOcr(blob_name, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    processor_id="e856b36daa605a77"
    result = Model(processor_id,blob)
    dict = {}
    for i in range(len(result)):
        dict[result[i].type_] = result[i].mention_text
    return dict


def CcOcr(blob_name, bucket_name):
    client = storage.Client()
    # Obtén el objeto del bucket
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    processor_id="d5b5b24ce5e59b1c"
    result = Model(processor_id,blob)
    dict = {}
    for i in range(len(result)):
        dict[result[i].type_] = result[i].mention_text
    return dict

def RutOcr(blob_name, bucket_name):
    client = storage.Client()
    # Obtén el objeto del bucket
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    processor_id="61028dc90ae32dcb"
    result = Model(processor_id,blob)
    dict = {}
    for i in range(len(result)):
        dict[result[i].type_] = result[i].mention_text
    return dict