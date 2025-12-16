from clusteConection import get_weaviate_client
from embeddings import get_embedding

def diagnosticar_problema():
    client = get_weaviate_client()
    collection = client.collections.get('Viaje')
    
    print("🔍 **DIAGNÓSTICO DEL SISTEMA**")
    print("="*50)
    
    # 1. Verificar cuántos documentos hay
    all_docs = collection.query.fetch_objects(limit=10, include_vector=True)
    print(f"📊 Total documentos: {len(all_docs.objects)}")
    
    # 2. Verificar si tienen vectores
    for i, obj in enumerate(all_docs.objects):
        has_vector = obj.vector is not None and len(obj.vector) > 0 if obj.vector else False
        desc = obj.properties.get('descripcion', 'N/A')[:100]
        rating = obj.properties.get('rating', 'N/A')
        destino = obj.properties.get('destino', 'N/A')
        
        print(f"\n📄 Documento {i+1}:")
        print(f"   Destino: {destino}")
        print(f"   Rating: {rating}")
        print(f"   Vector: {'✅ SÍ' if has_vector else '❌ NO'}")
        print(f"   Descripción: {desc}...")
    
    # 3. Probar embedding de consulta
    print(f"\n🧠 Probando embedding de consulta...")
    test_query = "recomiendame un viaje familiar con rating alto"
    query_emb = get_embedding(test_query)
    
    if query_emb:
        print(f"✅ Embedding generado: {len(query_emb)} dimensiones")
    else:
        print("❌ Error generando embedding de consulta")
        
    # 4. Probar búsqueda alternativa por texto
    print(f"\n🔤 Probando búsqueda por texto (BM25)...")
    try:
        text_results = collection.query.bm25(
            query="rating alto familiar",
            limit=5
        )
        print(f"📝 Búsqueda texto encontró: {len(text_results.objects)} documentos")
        
        for i, obj in enumerate(text_results.objects):
            props = obj.properties
            print(f"   {i+1}. {props.get('destino', 'N/A')} - Rating: {props.get('rating', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Error en búsqueda texto: {e}")
    
    client.close()

if __name__ == "__main__":
    diagnosticar_problema()