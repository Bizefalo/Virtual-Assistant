# Guía detallada del proyecto Weaviable

Esta guía explica el funcionamiento de los archivos principales del proyecto y cómo usarlos para procesar PDFs, extraer información, generar embeddings y realizar consultas con RAG (Retrieval Augmented Generation) usando Weaviate y OpenAI.

## Archivos principales

### 1. main.py
Este es el archivo principal que orquesta todo el flujo:
- **Conexión a Weaviate:**
  - Usa `get_weaviate_client()` para conectarse a la base de datos vectorial Weaviate.
  - Llama a `create_schema(client)` para definir la estructura de los datos.
- **Procesamiento de PDF:**
  - Usa `pdf_to_text("viajes_demo.pdf")` para extraer el texto de un PDF.
  - Divide el texto en fragmentos (chunks) con `chunk_text(texto)`.
- **Subida de datos:**
  - Define metadatos (destino, tipo de viaje, transporte, rating, duración).
  - Usa `upload_chunks(client, chunks, metadata)` para subir los fragmentos y metadatos a Weaviate.
- **Consulta RAG:**
  - Realiza una consulta con `query_rag(client, "Recomiéndame un destino familiar con rating alto")` y muestra el resultado.

### 2. clusteConection.py
- Define funciones para conectarse a Weaviate y crear el esquema de la base de datos.
- Permite que otros módulos interactúen con la base de datos vectorial.

### 3. pdfs.py
- Usa la librería `pypdf` para leer PDFs y extraer texto.
- Divide el texto en fragmentos para facilitar el procesamiento y la subida a Weaviate.

### 4. subir_chunks.py
- Define la función `upload_chunks` que toma los fragmentos de texto y los metadatos, y los sube a Weaviate.
- Utiliza embeddings generados por OpenAI para almacenar los datos de forma vectorial.

### 5. embeddings.py
- Usa la API de OpenAI para generar embeddings (representaciones vectoriales) de los fragmentos de texto.
- La clave de API se define directamente en el código para facilitar la configuración.

### 6. rag_query.py
- Permite realizar consultas semánticas sobre los datos almacenados en Weaviate usando RAG.
- Devuelve respuestas basadas en la información subida y los embeddings generados.

## Requisitos previos
- Python 3.13 instalado.
- Paquetes instalados: `openai`, `weaviate-client`, `pypdf`.
- Clave de API de OpenAI configurada en `embeddings.py`.

## Ejecución
1. Coloca tu PDF en la carpeta del proyecto y actualiza el nombre en `main.py` si es necesario.
2. Ejecuta el script principal:
   ```powershell
   C:/Users/viceg/AppData/Local/Programs/Python/Python313/python.exe main.py
   ```
3. El sistema procesará el PDF, subirá los datos a Weaviate y permitirá realizar consultas inteligentes sobre la información.

## Notas finales
- Puedes modificar los metadatos y el prompt de consulta en `main.py` para adaptarlo a otros casos de uso.
- El sistema está preparado para ser extendido y adaptado por otros estudiantes.

---

Si tienes dudas, revisa cada archivo y sigue la estructura explicada aquí. ¡Éxito en tus proyectos!
