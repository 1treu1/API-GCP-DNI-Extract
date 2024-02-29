from google.cloud import storage

def descargar_imagen(bucket_nombre, objeto_nombre, destino_local):
    # Crea un cliente de almacenamiento de Google Cloud
    client = storage.Client()

    # Obtén el objeto del bucket
    bucket = client.get_bucket(bucket_nombre)
    blob = bucket.blob(objeto_nombre)

    # Descarga el objeto a un archivo local
    blob.download_to_filename(destino_local)

# # Especifica el nombre del bucket, el nombre del objeto y la ubicación local
# bucket_nombre = 'bk-upload-documents-ocr-api'
# objeto_nombre = 'img.jpeg'
# destino_local = '/home/lhmedina/Documentos/API-GCP-DNI-Extract/Img/img.jpeg'

# # Descarga la imagen desde el bucket
# descargar_imagen(bucket_nombre, objeto_nombre, destino_local)
