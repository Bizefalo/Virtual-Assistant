from clusteConection import get_weaviate_client
import requests

client = get_weaviate_client()
collection = client.collections.get('Viaje')

# Búsqueda por texto (sin embeddings)
query = "rating alto familiar"

# Usar búsqueda BM25 (texto)
results = collection.query.bm25(
    query=query,
    limit=3
)

print('=== RESULTADOS DE BÚSQUEDA ===')
print(f'Total encontrados: {len(results.objects)}')

contextos = []
for i, obj in enumerate(results.objects):
    props = obj.properties
    print(f'\nResultado {i+1}:')
    print(f'  - Destino: {props.get("destino", "N/A")}')
    print(f'  - Rating: {props.get("rating", "N/A")}')
    print(f'  - Descripción: {props.get("descripcion", "N/A")[:150]}...')
    
    contextos.append(props.get("descripcion", ""))

# Crear prompt para Ollama
if contextos:
    prompt = f"Usa esta información para responder:\n{contextos}\n\nPregunta: Recomiéndame un destino familiar con rating alto"
    
    print('\n=== CONSULTANDO A OLLAMA ===')
    ollama_response = requests.post('http://localhost:11434/api/generate', 
        json={'model': 'llama3.1', 'prompt': prompt, 'stream': False})
    
    if ollama_response.status_code == 200:
        respuesta = ollama_response.json()['response']
        print('\n=== RESPUESTA FINAL ===')
        print(respuesta)
    else:
        print(f'Error: {ollama_response.text}')
else:
    print('No se encontraron resultados')

client.close()