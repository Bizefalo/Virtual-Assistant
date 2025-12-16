
def upload_chunks(client, chunks, metadata=None):
    metadata = metadata or {}
    
    for i, chunk in enumerate(chunks):
        print(f"📤 Subiendo chunk {i+1}/{len(chunks)}...")
        
        # Generar embedding usando Ollama
        from embeddings import get_embedding
        embedding = get_embedding(chunk)
        
        data_obj = {
            **metadata,
            "descripcion": chunk,
            "chunk_index": i,
            "total_chunks": len(chunks)
        }
        
        # Insertar CON embedding
        if embedding:
            client.collections.get("Viaje").data.insert(data_obj, vector=embedding)
            print(f"✅ Chunk {i+1} subido CON embedding")
        else:
            client.collections.get("Viaje").data.insert(data_obj)
            print(f"⚠️ Chunk {i+1} subido SIN embedding")
    
    print(f"🎉 Todos los {len(chunks)} chunks han sido subidos!")
