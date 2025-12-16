# 🚀 WEAVIABLE - Sistema RAG con Weaviate y Ollama

## 📁 Estructura del Proyecto

```
Weaviable/
│
├── 📄 clusteConection.py          # Conexión y configuración de Weaviate
├── 📄 main.py                     # Script principal de ejecución
├── 📄 pdfs.py                     # Procesamiento de PDFs
├── 📄 subir_chunks.py             # Subida de datos con embeddings
├── 📄 embeddings.py               # Generación de embeddings con Ollama
├── 📄 rag_query.py                # Consultas RAG con búsqueda vectorial
├── 📄 chat_interactivo.py         # 🌟 Interfaz interactiva principal
│
├── 🐳 docker-compose.yml          # Configuración de Weaviate local
├── 📖 viajes_demo.pdf             # Archivo PDF de ejemplo
│
├── 🔧 Scripts de utilidad:
│   ├── diagnostico.py             # Diagnóstico del sistema
│   ├── test_query.py              # Pruebas de consultas
│   ├── test_search.py             # Pruebas de búsqueda
│   ├── limpiar_datos.py           # Limpieza de datos
│   ├── probar_embeddings.py       # Pruebas de embeddings
│   ├── consultas_demo.py          # Demo de consultas múltiples
│   └── verificar_campos.py        # Verificación de campos disponibles
│
└── 📚 Documentación:
    └── ESTRUCTURA_PROYECTO.md     # Este archivo
```

## 🏗️ Arquitectura del Sistema

### 🔄 Flujo de Datos
```
PDF Input → Text Extraction → Text Chunking → Embedding Generation → Weaviate Storage
    ↓
Query Input → Query Embedding → Vector Search → Context Retrieval → Ollama Response
```

### 🧩 Componentes Principales

#### 1. **🔌 Conexión (clusteConection.py)**
- Conecta a Weaviate local (Docker)
- Crea esquema de datos
- Valida conexión

#### 2. **📖 Procesamiento (pdfs.py)**
- Extrae texto de PDFs
- Divide en chunks manejables
- Prepara datos para vectorización

#### 3. **🧠 Embeddings (embeddings.py)**
- Genera vectores usando Ollama
- Modelo: llama3.1 (4096 dimensiones)
- API local: http://localhost:11434

#### 4. **💾 Almacenamiento (subir_chunks.py)**
- Inserta datos con vectores
- Metadatos estructurados
- Progreso visual

#### 5. **🔍 Consultas (rag_query.py)**
- Búsqueda vectorial (near_vector)
- Búsqueda híbrida (BM25 + vectorial)
- Retrieval de contexto relevante

#### 6. **💬 Interfaz (chat_interactivo.py)**
- Chat interactivo en terminal
- Búsqueda inteligente
- Respuestas de Ollama

## ⚙️ Configuración Técnica

### 🐳 Docker (Weaviate Local)
```yaml
# docker-compose.yml
services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:1.25.7
    ports: ["8080:8080", "50051:50051"]
    environment:
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      DEFAULT_VECTORIZER_MODULE: 'text2vec-ollama'
      TEXT2VEC_OLLAMA_API_ENDPOINT: 'http://host.docker.internal:11434'
```

### 🤖 Modelos de Ollama
- **llama3.1** (4.9GB) - Embeddings y generación
- **gemma3:1b** (815MB) - Alternativa ligera

### 📊 Esquema de Datos
```python
{
    "destino": DataType.TEXT,
    "tipo_viaje": DataType.TEXT,
    "transporte": DataType.TEXT,
    "rating": DataType.NUMBER,
    "duracion": DataType.TEXT,
    "descripcion": DataType.TEXT,
    "chunk_index": DataType.NUMBER,
    "total_chunks": DataType.NUMBER
}
```

## 🚀 Comandos de Uso

### Inicializar Sistema
```bash
# 1. Levantar Weaviate
docker-compose up -d

# 2. Procesar y subir datos
python main.py

# 3. Usar chat interactivo
python chat_interactivo.py
```

### Utilidades
```bash
# Diagnóstico completo
python diagnostico.py

# Limpiar datos
python limpiar_datos.py

# Probar consultas
python test_search.py
```

## 🎯 Capacidades del Sistema

### ✅ **Funcionalidades Implementadas**
- 📖 Procesamiento de PDFs
- 🧠 Generación de embeddings con Ollama
- 💾 Almacenamiento vectorial en Weaviate
- 🔍 Búsqueda híbrida (vectorial + texto)
- 💬 Interfaz interactiva
- 🤖 Respuestas inteligentes con LLM

### 📊 **Tipos de Consultas Soportadas**
- Búsqueda por similitud semántica
- Filtrado por rating, destino, tipo
- Comparaciones entre opciones
- Recomendaciones personalizadas

### 🛠️ **Herramientas de Diagnóstico**
- Verificación de conexiones
- Análisis de datos almacenados
- Pruebas de embeddings
- Monitoreo de rendimiento

## 🔧 Dependencias

### Python Packages
```
weaviate-client==4.16.10
pypdf
requests
```

### Servicios Externos
- Docker Desktop
- Ollama (local)
- Weaviate (Docker container)

## 📈 Métricas del Sistema
- **Documentos procesados**: 4 chunks
- **Dimensión de embeddings**: 4096
- **Modelos disponibles**: 2 (llama3.1, gemma3:1b)
- **Tiempo de respuesta**: ~10-30 segundos

## 🎉 Estado Actual
✅ **Sistema completamente funcional**  
✅ **Weaviate local operativo**  
✅ **Ollama integrado**  
✅ **Embeddings funcionando**  
✅ **Chat interactivo listo**  
✅ **Búsqueda híbrida implementada**

---
*Proyecto creado: 25 de septiembre, 2025*  
*Tecnologías: Python, Weaviate, Ollama, Docker*