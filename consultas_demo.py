from clusteConection import get_weaviate_client
import requests
import json

def consultar_viajes(pregunta):
    """Función para hacer consultas RAG optimizadas"""
    client = get_weaviate_client()
    collection = client.collections.get('Viaje')

    try:
        # Búsqueda por texto (BM25)
        results = collection.query.bm25(
            query=pregunta,
            limit=3,
            return_metadata=['score']
        )

        print(f'✅ Encontrados {len(results.objects)} documentos relevantes')
        
        # Preparar contexto
        contextos = []
        for obj in results.objects:
            descripcion = obj.properties.get("descripcion", "")
            destino = obj.properties.get("destino", "N/A")
            rating = obj.properties.get("rating", "N/A")
            contextos.append(f"Destino: {destino}, Rating: {rating}, Descripción: {descripcion[:200]}")

        if not contextos:
            return "❌ No se encontraron documentos relacionados con tu consulta."

        # Crear prompt optimizado
        prompt = f"""Basándote en esta información sobre viajes, responde de forma concisa y útil:

INFORMACIÓN DISPONIBLE:
{chr(10).join(contextos)}

PREGUNTA: {pregunta}

Responde de forma directa y práctica:"""

        # Consultar Ollama
        print('🤖 Consultando a Ollama...')
        ollama_response = requests.post('http://localhost:11434/api/generate', 
            json={
                'model': 'llama3.1', 
                'prompt': prompt, 
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'max_tokens': 300
                }
            }, timeout=60)

        if ollama_response.status_code == 200:
            respuesta = ollama_response.json()['response']
            return f"💡 **Respuesta:** {respuesta.strip()}"
        else:
            return f"❌ Error en Ollama: {ollama_response.text}"
            
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        client.close()

if __name__ == "__main__":
    # Ejemplos de consultas
    consultas = [
        "Recomiéndame un destino familiar con rating alto",
        "¿Qué viajes de aventura hay disponibles?",
        "Busco un destino romántico para pareja",
        "¿Cuál es el viaje con mejor rating?"
    ]
    
    print("🚀 **SISTEMA RAG - CONSULTAS DE VIAJES** 🚀\n")
    
    for i, consulta in enumerate(consultas, 1):
        print(f"📋 **Consulta {i}:** {consulta}")
        print("-" * 60)
        resultado = consultar_viajes(consulta)
        print(resultado)
        print("\n" + "="*80 + "\n")