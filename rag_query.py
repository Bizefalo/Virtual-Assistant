def query_rag(client, query, top_k=5):
    from embeddings import get_embedding
    query_emb = get_embedding(query)
    
    if query_emb is None:
        return f"Error obteniendo embedding. Pregunta original: {query}"

    # Usar la nueva sintaxis de Weaviate v4
    collection = client.collections.get("Viaje")
    
    results = collection.query.near_vector(
        near_vector=query_emb,
        limit=top_k,
        return_metadata=['score']
    )

    # Extraer contextos de los resultados
    contextos = []
    for item in results.objects:
        contextos.append(item.properties.get("descripcion", "Sin descripción"))

    if not contextos:
        contextos = ["No se encontraron documentos relacionados."]

    prompt = f"Usa esta información para responder:\n{contextos}\n\nPregunta: {query}"
    return prompt  # Luego pasas 'prompt' a LLaMA 3.1
