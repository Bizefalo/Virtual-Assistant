from clusteConection import get_weaviate_client
from rag_query import query_rag
import requests

def probar_consulta_con_embeddings():
    client = get_weaviate_client()
    
    # Consulta de prueba
    consulta = "Recomiéndame un destino familiar con rating alto"
    
    print("🔍 Realizando búsqueda vectorial...")
    prompt = query_rag(client, consulta)
    
    print("📋 CONTEXTO ENCONTRADO:")
    print("-" * 50)
    print(prompt)
    print("-" * 50)
    
    # Enviar a Ollama
    print("🤖 Enviando a Ollama...")
    try:
        response = requests.post('http://localhost:11434/api/generate',
            json={
                'model': 'llama3.1', 
                'prompt': prompt, 
                'stream': False
            }, timeout=120)
        
        if response.status_code == 200:
            respuesta = response.json()['response']
            print("\n💡 RESPUESTA FINAL:")
            print("=" * 50)
            print(respuesta)
            print("=" * 50)
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    client.close()

if __name__ == "__main__":
    probar_consulta_con_embeddings()