# 📚 GUÍA COMPLETA: Construyendo un Sistema RAG con Weaviate y Ollama

## 🎯 **¿Qué vamos a construir?**
Un sistema RAG (Retrieval-Augmented Generation) que:
- 📖 Lee documentos PDF
- 🧠 Los convierte en embeddings con IA
- 💾 Los almacena en una base de datos vectorial
- 🔍 Permite hacer consultas inteligentes
- 💬 Responde usando un LLM local

---

## 📋 **PRERREQUISITOS**

### 1. **Sistema Operativo**: Windows 10/11
### 2. **Software requerido**:
- ✅ Python 3.11+ instalado
- ✅ Docker Desktop instalado
- ✅ Git (opcional)

---

## 🚀 **PASO 1: Configuración Inicial**

### 1.1 Crear directorio del proyecto
```bash
mkdir Weaviable
cd Weaviable
```

### 1.2 Instalar paquetes de Python
```bash
pip install weaviate-client==4.16.10 pypdf requests
```

### 1.3 Verificar instalaciones
```bash
python --version
docker --version
```

---

## 🤖 **PASO 2: Instalar y Configurar Ollama**

### 2.1 Descargar Ollama
```bash
# Ir a: https://ollama.ai/download
# Descargar e instalar Ollama para Windows
```

### 2.2 Iniciar Ollama
```bash
# Abrir nueva terminal PowerShell
ollama serve
```

### 2.3 Descargar modelos
```bash
# En otra terminal
ollama pull llama3.1
ollama pull gemma3:1b
```

### 2.4 Verificar modelos
```bash
ollama list
```
**Resultado esperado:**
```
NAME               ID              SIZE      MODIFIED     
gemma3:1b          8648f39daa8f    815 MB    2 hours ago
llama3.1:latest    46e0c10c039e    4.9 GB    2 hours ago
```

---

## 🐳 **PASO 3: Configurar Weaviate con Docker**

### 3.1 Crear docker-compose.yml
```yaml
# Archivo: docker-compose.yml
version: '3.4'
services:
  weaviate:
    command:
    - --host
    - 0.0.0.0
    - --port
    - '8080'
    - --scheme
    - http
    image: cr.weaviate.io/semitechnologies/weaviate:1.25.7
    ports:
    - "8080:8080"
    - "50051:50051"
    volumes:
    - weaviate_data:/var/lib/weaviate
    restart: on-failure:0
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/var/lib/weaviate'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-ollama'
      ENABLE_MODULES: 'text2vec-ollama'
      CLUSTER_HOSTNAME: 'node1'
      TEXT2VEC_OLLAMA_API_ENDPOINT: 'http://host.docker.internal:11434'
volumes:
  weaviate_data:
```

### 3.2 Levantar Weaviate
```bash
docker-compose up -d
```

### 3.3 Verificar que funcione
```bash
docker-compose ps
```
**Resultado esperado:**
```
✔ Container weaviable-weaviate-1  Started
```

---

## 📝 **PASO 4: Crear los Scripts de Python**

### 4.1 Conexión a Weaviate (clusteConection.py)
```python
# Archivo: clusteConection.py
import os
import weaviate

# Validar la conexión a Weaviate
def validate_connection(client):
    try:
        if client.is_ready():
            print("Conexión exitosa a Weaviate local.")
            return True
        else:
            print("No se pudo conectar a Weaviate local.")
            return False
    except Exception as e:
        print("Error de conexión:", e)
        return False

def get_weaviate_client():
    # Conectar a Weaviate local (Docker) - sin autenticación
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080
    )
    return client

def create_schema(client):
    # Definir los campos de la colección
    from weaviate.classes.config import Configure, DataType
    viaje_properties = [
        {"name": "destino", "data_type": DataType.TEXT},
        {"name": "tipo_viaje", "data_type": DataType.TEXT},
        {"name": "transporte", "data_type": DataType.TEXT},
        {"name": "rating", "data_type": DataType.NUMBER},
        {"name": "duracion", "data_type": DataType.TEXT},
        {"name": "descripcion", "data_type": DataType.TEXT}
    ]
    try:
        # Eliminar colección existente si existe
        client.collections.delete("Viaje")
    except:
        pass
    
    # Crear nueva colección sin vectorizador automático (para probar primero)
    client.collections.create(
        name="Viaje",
        properties=viaje_properties
    )

if __name__ == "__main__":
    client = get_weaviate_client()
    validate_connection(client)
    client.close()
```

### 4.2 Procesamiento de PDFs (pdfs.py)
```python
# Archivo: pdfs.py
from pypdf import PdfReader
import re

def pdf_to_text(pdf_path):
    """Extrae texto de un archivo PDF"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error leyendo PDF: {e}")
        return ""

def chunk_text(text, chunk_size=1000, overlap=200):
    """Divide el texto en chunks manejables"""
    # Limpiar el texto
    text = re.sub(r'\s+', ' ', text.strip())
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Si no es el último chunk, buscar un espacio para cortar
        if end < len(text):
            # Buscar el último espacio antes del límite
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Overlap para mantener contexto
        start = end - overlap
    
    return chunks

if __name__ == "__main__":
    # Ejemplo de uso
    texto = pdf_to_text("viajes_demo.pdf")
    chunks = chunk_text(texto)
    print(f"PDF procesado: {len(chunks)} chunks generados")
    for i, chunk in enumerate(chunks[:2]):  # Mostrar primeros 2
        print(f"\nChunk {i+1}: {chunk[:100]}...")
```

### 4.3 Generación de Embeddings (embeddings.py)
```python
# Archivo: embeddings.py
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
```

### 4.4 Subida de Datos (subir_chunks.py)
```python
# Archivo: subir_chunks.py

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
```

### 4.5 Consultas RAG (rag_query.py)
```python
# Archivo: rag_query.py
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
```

### 4.6 Script Principal (main.py)
```python
# Archivo: main.py
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
import requests
prompt = query_rag(client, "Recomiéndame un destino familiar con rating alto")
ollama_url = "http://localhost:11434/api/generate"
ollama_payload = {
    "model": "llama3.1",
    "prompt": prompt,
    "stream": False
}

print("🤖 Consultando a Ollama...")
try:
    response = requests.post(ollama_url, json=ollama_payload, timeout=60)
    if response.status_code == 200:
        result = response.json()
        print("💡 Respuesta:", result['response'])
    else:
        print("Error:", response.text)
except Exception as e:
    print("Error:", e)

client.close()
```

---

## 🎮 **PASO 5: Chat Interactivo (Opcional pero Recomendado)**

### 5.1 Chat Interactivo (chat_interactivo.py)
```python
# Archivo: chat_interactivo.py
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
                print("🔤 Usando búsqueda por texto (BM25)...")
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
```

---

## 📖 **PASO 6: Crear un PDF de Ejemplo**

### 6.1 Crear viajes_demo.pdf
```
Puedes crear un PDF simple con este contenido:

Catálogo de 100 Viajes (Demo)

1. Toronto - Aventura - Barco - Rating: 1.7 - 12 días
   Descripción: Explora los grandes lagos de Canadá en una aventura acuática única.

2. Barcelona - Relax - Bus - Rating: 4.0 - 7 días  
   Descripción: Disfruta de la arquitectura de Gaudí y las playas mediterráneas.

3. Ciudad de México - Romántico - Auto - Rating: 3.8 - 12 días
   Descripción: Descubre la cultura prehispánica y la gastronomía mexicana.

4. Tokio - Cultural - Tren - Rating: 3.3 - 8 días
   Descripción: Sumérgete en la tradición japonesa y la modernidad de Tokio.

5. París - Relax - Auto - Rating: 4.7 - 6 días
   Descripción: La ciudad del amor con sus museos, cafés y arquitectura única.
```

---

## 🚀 **PASO 7: Ejecutar el Sistema**

### 7.1 Orden de ejecución
```bash
# Terminal 1: Mantener Ollama corriendo
ollama serve

# Terminal 2: Levantar Weaviate
docker-compose up -d

# Terminal 3: Procesar y subir datos
python main.py

# Terminal 4: Usar chat interactivo
python chat_interactivo.py
```

### 7.2 Verificar que todo funcione
```bash
# Verificar Ollama
ollama list

# Verificar Docker
docker-compose ps

# Verificar conexión Python
python clusteConection.py
```

---

## 🎯 **PASO 8: Ejemplos de Consultas**

### Consultas que puedes probar:
1. `"Recomiéndame un viaje familiar con rating alto"`
2. `"¿Qué viajes de aventura hay disponibles?"`
3. `"Busco un destino romántico"`
4. `"¿Cuál es el mejor destino según rating?"`
5. `"¿Qué opciones de transporte hay?"`
6. `"Muéstrame viajes de más de 10 días"`

---

## 🔧 **PASO 9: Herramientas de Diagnóstico**

### 9.1 Script de Diagnóstico (diagnostico.py)
```python
# Archivo: diagnostico.py
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
    
    client.close()

if __name__ == "__main__":
    diagnosticar_problema()
```

### 9.2 Script de Limpieza (limpiar_datos.py)
```python
# Archivo: limpiar_datos.py
from clusteConection import get_weaviate_client

# Conectar y limpiar datos existentes
client = get_weaviate_client()

try:
    # Eliminar colección completa
    client.collections.delete("Viaje")
    print("✅ Colección 'Viaje' eliminada exitosamente")
except Exception as e:
    print(f"⚠️ Error eliminando colección: {e}")

client.close()
print("🔄 Ahora puedes volver a ejecutar main.py para resubir con embeddings")
```

---

## 🏆 **PASO 10: Verificación Final**

### 10.1 Checklist de funcionamiento
- [ ] ✅ Docker Desktop corriendo
- [ ] ✅ Ollama serve ejecutándose
- [ ] ✅ Weaviate contenedor activo
- [ ] ✅ Modelos descargados (llama3.1)
- [ ] ✅ PDF de ejemplo creado
- [ ] ✅ Todos los scripts Python creados
- [ ] ✅ Datos subidos exitosamente
- [ ] ✅ Chat interactivo funcionando

### 10.2 Comandos de verificación
```bash
# Verificar servicios
docker-compose ps
ollama list
python diagnostico.py

# Probar sistema completo
python chat_interactivo.py
```

---

## 🔄 **PASO 11: Reiniciar el Sistema (Para Uso Futuro)**

### 11.1 **Reinicio Completo (Desde Cero)**
```bash
# 1. Limpiar todo
docker-compose down
python limpiar_datos.py

# 2. Reiniciar servicios (4 terminales)
# Terminal 1:
ollama serve

# Terminal 2:
docker-compose up -d

# Terminal 3:
python main.py

# Terminal 4:
python chat_interactivo.py
```

### 11.2 **Reinicio Rápido (Solo Servicios)**
```bash
# Si los servicios se cerraron pero los datos están bien:
docker-compose restart
ollama serve  # Solo si no está corriendo
python chat_interactivo.py
```

### 11.3 **Verificación Rápida**
```bash
# Verificar que todo funcione:
docker-compose ps        # ✅ Weaviate corriendo
ollama list             # ✅ Modelos disponibles  
python diagnostico.py   # ✅ Datos y conexiones OK
```

### 11.4 **Orden Correcto de Inicio**
```
1. ollama serve          (Primero - en terminal separado)
2. docker-compose up -d  (Segundo - Weaviate)
3. python main.py        (Tercero - Solo si necesitas resubir datos)
4. python chat_interactivo.py  (Cuarto - Para usar el sistema)
```

---

## 🎓 **CONCEPTOS APRENDIDOS**

### Tecnologías utilizadas:
1. **RAG (Retrieval-Augmented Generation)** - Técnica de IA para mejorar respuestas
2. **Embeddings** - Representación vectorial de texto
3. **Weaviate** - Base de datos vectorial
4. **Ollama** - Servidor local de LLMs
5. **Docker** - Contenedorización
6. **Python** - Procesamiento y APIs

### Flujo de datos:
```
PDF → Chunks → Embeddings → Weaviate → Query → Context → LLM → Response
```

---

## ❗ **SOLUCIÓN DE PROBLEMAS COMUNES**

### Problema 1: "Connection refused" en Ollama
**Solución:**
```bash
# Verificar que Ollama esté corriendo
ollama serve

# En otra terminal, verificar modelos
ollama list
```

### Problema 2: Docker no inicia
**Solución:**
```bash
# Verificar Docker Desktop esté corriendo
docker --version
docker-compose up -d --force-recreate
```

### Problema 3: "No se encontraron documentos"
**Solución:**
```bash
# Limpiar y resubir datos
python limpiar_datos.py
python main.py
```

### Problema 4: Embeddings no se generan
**Solución:**
```bash
# Verificar modelo compatible
ollama pull llama3.1
# Cambiar modelo en embeddings.py si es necesario
```

---

## 🎉 **¡FELICITACIONES!**

Has construido exitosamente un sistema RAG completo con:
- ✅ **Procesamiento de documentos**
- ✅ **Base de datos vectorial**
- ✅ **LLM local**
- ✅ **Interfaz de consultas**
- ✅ **Búsqueda semántica**

**Tu sistema puede:**
- 📖 Leer y procesar PDFs
- 🧠 Generar embeddings inteligentes
- 💾 Almacenar conocimiento vectorialmente
- 🔍 Buscar información relevante
- 💬 Responder preguntas naturalmente

---

*Guía creada: 25 de septiembre, 2025*  
*Duración estimada: 2-3 horas*  
*Nivel: Intermedio*