
import requests
import json

def get_embedding(text):
    """Obtener embedding usando Ollama local"""
    try:
        response = requests.post('http://localhost:11434/api/embed',
                                json={'model': 'llama3.1', 'input': text})
        
        if response.status_code == 200:
            return response.json()['embeddings'][0]
        else:
            print(f"Error obteniendo embedding: {response.text}")
            return None
    except Exception as e:
        print(f"Error conectando con Ollama: {e}")
        return None

