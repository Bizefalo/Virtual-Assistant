from clusteConection import get_weaviate_client
from embeddings import get_embedding
import requests
import json

def hacer_consulta_interactiva():
    print("🚀 **SISTEMA RAG INTERACTIVO** 🚀")
    print("Conectando a Weaviate y Ollama...")
    
    client = get_weaviate_client()
    collection = client.collections.get('Viaje')
    
    # Verificar datos
    total_docs = collection.query.fetch_objects(limit=1)
    print(f"✅ Conectado! Documentos disponibles: {len(total_docs.objects)}")
    
    print("\n" + "="*60)
    print("💬 **ESCRIBE TU CONSULTA** (o 'salir' para terminar)")
    print("="*60)
    
    while True:
        consulta = input("\n🔍 Tu pregunta: ").strip()
        
        if consulta.lower() in ['salir', 'exit', 'quit', '']:
            print("👋 ¡Hasta luego!")
            break
            
        print(f"\n🔄 Procesando: '{consulta}'...")
        
        try:
            # Generar embedding de la consulta
            query_embedding = get_embedding(consulta)
            
            # OPCIÓN 1: Probar búsqueda vectorial
            results = None
            if query_embedding:
                print("🔍 Intentando búsqueda vectorial...")
                try:
                    results = collection.query.near_vector(
                        near_vector=query_embedding,
                        limit=3,
                        distance=0.8,  # Umbral más permisivo
                        return_metadata=['distance']
                    )
                    if results.objects:
                        print(f"✅ Búsqueda vectorial: {len(results.objects)} documentos")
                except Exception as e:
                    print(f"⚠️ Búsqueda vectorial falló: {e}")
            
            # OPCIÓN 2: Si vectorial falla, usar búsqueda por texto
            if not results or not results.objects:
                print("� Usando búsqueda por texto (BM25)...")
                results = collection.query.bm25(
                    query=consulta,
                    limit=3
                )
                print(f"✅ Búsqueda texto: {len(results.objects)} documentos")
            
            if not results or not results.objects:
                print("❌ No se encontraron documentos relacionados")
                continue
            
            # Preparar contexto
            contextos = []
            print(f"📚 Encontrados {len(results.objects)} documentos relevantes:")
            
            for i, obj in enumerate(results.objects):
                props = obj.properties
                contexto = f"Destino: {props.get('destino', 'N/A')}, Rating: {props.get('rating', 'N/A')}, Descripción: {props.get('descripcion', '')[:200]}..."
                contextos.append(contexto)
                print(f"  {i+1}. {props.get('destino', 'N/A')} (Rating: {props.get('rating', 'N/A')})")
            
            # Crear prompt para Ollama
            prompt = f"""Basándote SOLO en esta información sobre viajes, responde de forma concisa:

INFORMACIÓN:
{chr(10).join(contextos)}

PREGUNTA: {consulta}

Respuesta:"""
            
            print("\n🤖 Consultando a Ollama...")
            
            # Enviar a Ollama
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.1',
                    'prompt': prompt,
                    'stream': False,
                    'options': {'temperature': 0.7}
                }, timeout=60)
            
            if response.status_code == 200:
                respuesta = response.json()['response'].strip()
                print("\n" + "="*60)
                print(f"💡 **RESPUESTA:**")
                print(respuesta)
                print("="*60)
            else:
                print(f"❌ Error en Ollama: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    client.close()

if __name__ == "__main__":
    hacer_consulta_interactiva()