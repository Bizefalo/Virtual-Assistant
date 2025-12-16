from clusteConection import get_weaviate_client, create_schema, validate_connection
from pdfs import pdf_to_text, chunk_text
from subir_chunks import upload_chunks
from rag_query import query_rag

client = get_weaviate_client()
validate_connection(client)
create_schema(client)

# Leer PDF
texto = pdf_to_text("viajes_demo.pdf")
chunks = chunk_text(texto)

# Subir a Weaviate
metadata = {
    "destino": "París",
    "tipo_viaje": "Cultural",
    "transporte": "Avión",
    "rating": 4.7,
    "duracion": "5 días"
}
upload_chunks(client, chunks, metadata)

# Ejemplo de consulta

# Enviar el prompt a Ollama (Llama)
import requests
prompt = query_rag(client, "Recomiéndame un destino familiar con rating alto")
ollama_url = "http://localhost:11434/api/generate"
ollama_payload = {
    "model": "llama3.1",  # Cambia el nombre si usas otro modelo
    "prompt": prompt
}
response = requests.post(ollama_url, json=ollama_payload)
if response.ok:
    result = response.json()
    print("Respuesta de Llama:", result.get("response", "Sin respuesta"))
else:
    print("Error al consultar Ollama:", response.text)

# Cerrar la conexión con Weaviate
client.close()

client.schema().get()

client.close()
