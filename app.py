from flask import Flask, render_template, request, jsonify
import weaviate
from embeddings import get_embedding
import requests

app = Flask(__name__)

def conectar_weaviate():
    """Conecta a Weaviate local"""
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080
    )
    return client

def buscar_documentos(pregunta_usuario):
    """Busca documentos relevantes usando búsqueda híbrida"""
    client = conectar_weaviate()
    
    try:
        collection = client.collections.get("Viaje")
        
        # Primero intentar búsqueda vectorial
        query_embedding = get_embedding(pregunta_usuario)
        
        response = collection.query.near_vector(
            near_vector=query_embedding,
            limit=3,
            return_properties=["destino", "descripcion", "rating", "tipo_viaje", "transporte", "duracion"]
        )
        
        documentos = []
        if response.objects:
            for obj in response.objects:
                documentos.append({
                    "destino": obj.properties.get("destino", ""),
                    "descripcion": obj.properties.get("descripcion", ""),
                    "rating": obj.properties.get("rating", ""),
                    "tipo_viaje": obj.properties.get("tipo_viaje", ""),
                    "transporte": obj.properties.get("transporte", ""),
                    "duracion": obj.properties.get("duracion", "")
                })
        
        # Si no hay resultados, intentar búsqueda BM25
        if not documentos:
            response_bm25 = collection.query.bm25(
                query=pregunta_usuario,
                limit=3,
                return_properties=["destino", "descripcion", "rating", "tipo_viaje", "transporte", "duracion"]
            )
            
            if response_bm25.objects:
                for obj in response_bm25.objects:
                    documentos.append({
                        "destino": obj.properties.get("destino", ""),
                        "descripcion": obj.properties.get("descripcion", ""),
                        "rating": obj.properties.get("rating", ""),
                        "tipo_viaje": obj.properties.get("tipo_viaje", ""),
                        "transporte": obj.properties.get("transporte", ""),
                        "duracion": obj.properties.get("duracion", "")
                    })
        
        return documentos
    
    finally:
        client.close()

def generar_respuesta(pregunta, contexto_docs):
    """Genera respuesta usando Ollama"""
    contexto = "\n\n".join([
        f"Destino: {doc['destino']}\n"
        f"Tipo de viaje: {doc['tipo_viaje']}\n"
        f"Transporte: {doc['transporte']}\n"
        f"Duración: {doc['duracion']}\n"
        f"Rating: {doc['rating']}\n"
        f"Descripción: {doc['descripcion']}"
        for doc in contexto_docs
    ])
    
    prompt = f"""Eres un asistente de viajes. Usa la siguiente información para responder la pregunta del usuario.

Información disponible:
{contexto}

Pregunta del usuario: {pregunta}

Responde de manera amigable y concisa basándote únicamente en la información proporcionada. Si no hay información relevante, indica que no tienes esos datos."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
    )
    
    return response.json()["response"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        pregunta = data.get('pregunta', '')
        
        if not pregunta:
            return jsonify({'error': 'No se proporcionó ninguna pregunta'}), 400
        
        # Buscar documentos relevantes
        documentos = buscar_documentos(pregunta)
        
        if not documentos:
            respuesta = "Lo siento, no encontré información relevante sobre eso en mi base de datos de viajes."
        else:
            # Generar respuesta con Ollama
            respuesta = generar_respuesta(pregunta, documentos)
        
        return jsonify({
            'respuesta': respuesta,
            'documentos_encontrados': len(documentos)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
