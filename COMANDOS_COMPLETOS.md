# 📋 LISTA COMPLETA DE COMANDOS - Weaviable

## 🚀 **ORDEN DE EJECUCIÓN COMPLETO**

### **FASE 1: PREPARACIÓN DEL ENTORNO**

#### 1.1 Crear directorio del proyecto
```bash
mkdir Weaviable
cd Weaviable
```

#### 1.2 Instalar dependencias Python
```bash
pip install weaviate-client==4.16.10 pypdf requests
```

#### 1.3 Verificar instalaciones
```bash
python --version
docker --version
```

---

### **FASE 2: CONFIGURACIÓN DE OLLAMA**

#### 2.1 Iniciar Ollama (Terminal 1 - mantener abierto)
```bash
ollama serve
```

#### 2.2 Descargar modelos (en Terminal 2)
```bash
ollama pull llama3.1
ollama pull gemma3:1b
```

#### 2.3 Verificar modelos instalados
```bash
ollama list
```

#### 2.4 Verificar que Ollama esté corriendo
```bash
netstat -an | findstr :11434
```

---

### **FASE 3: CONFIGURACIÓN DE WEAVIATE**

#### 3.1 Levantar Weaviate con Docker (Terminal 3)
```bash
docker-compose up -d
```

#### 3.2 Verificar que Weaviate esté corriendo
```bash
docker-compose ps
```

#### 3.3 Verificar puerto de Weaviate
```bash
netstat -an | findstr :8080
```

---

### **FASE 4: PROCESAMIENTO INICIAL DE DATOS**

#### 4.1 Ejecutar script principal (procesar PDF y subir datos)
```bash
python main.py
```

#### 4.2 Verificar conexión a Weaviate (opcional)
```bash
python clusteConection.py
```

#### 4.3 Diagnosticar el sistema (opcional)
```bash
python diagnostico.py
```

---

### **FASE 5: USO DEL SISTEMA**

#### 5.1 Iniciar chat interactivo (Terminal 4)
```bash
python chat_interactivo.py
```

#### Ejemplos de consultas en el chat:
```
🔍 Tu pregunta: Recomiéndame un viaje familiar con rating alto
🔍 Tu pregunta: ¿Qué destinos son mejores para aventura?
🔍 Tu pregunta: Busco algo romántico para mi pareja
🔍 Tu pregunta: ¿Cuál es el viaje con mejor rating?
🔍 Tu pregunta: salir
```

---

## 🔄 **COMANDOS DE REINICIO**

### **Reinicio Completo (desde cero)**
```bash
# 1. Parar servicios
docker-compose down
# Ctrl+C en terminal de Ollama

# 2. Limpiar datos (opcional)
python limpiar_datos.py

# 3. Reiniciar servicios
ollama serve                    # Terminal 1
docker-compose up -d           # Terminal 2

# 4. Procesar datos (si se limpiaron)
python main.py                 # Terminal 3

# 5. Usar sistema
python chat_interactivo.py     # Terminal 4
```

### **Reinicio Rápido (mantener datos)**
```bash
# 1. Reiniciar servicios
ollama serve                    # Terminal 1 (si no está corriendo)
docker-compose restart         # Terminal 2

# 2. Usar sistema directamente
python chat_interactivo.py     # Terminal 3
```

---

## 🔧 **COMANDOS DE DIAGNÓSTICO Y MANTENIMIENTO**

### **Verificación de Estado**
```bash
# Verificar Docker
docker-compose ps

# Verificar Ollama
ollama list

# Diagnóstico completo del sistema
python diagnostico.py

# Verificar datos en Weaviate
python -c "from clusteConection import get_weaviate_client; client = get_weaviate_client(); collection = client.collections.get('Viaje'); results = collection.query.fetch_objects(limit=1); print(f'Documentos: {len(results.objects)}'); client.close()"

# Verificar conexión Weaviate
python -c "from clusteConection import get_weaviate_client, validate_connection; client = get_weaviate_client(); validate_connection(client); client.close()"
```

### **Limpieza y Mantenimiento**
```bash
# Limpiar datos de Weaviate
python limpiar_datos.py

# Parar todos los servicios
docker-compose down

# Limpiar Docker completamente
docker-compose down --volumes
docker system prune -f

# Verificar puertos libres
netstat -an | findstr :8080
netstat -an | findstr :11434
```

---

## 🆘 **COMANDOS DE EMERGENCIA**

### **Si algo está muy roto**
```bash
# 1. Matar todos los procesos
docker-compose down --volumes
taskkill /f /im ollama.exe

# 2. Limpiar completamente
docker system prune -a -f
docker volume prune -f

# 3. Empezar desde cero
ollama serve
docker-compose up -d
python main.py
python chat_interactivo.py
```

### **Si hay problemas de conexión**
```bash
# Verificar servicios
docker-compose ps
ollama list

# Reiniciar servicios específicos
docker-compose restart
ollama serve

# Verificar puertos
netstat -an | findstr :8080
netstat -an | findstr :11434
```

---

## 📊 **COMANDOS DE PRUEBA Y VALIDACIÓN**

### **Probar componentes individualmente**
```bash
# Probar conexión Weaviate
python clusteConection.py

# Probar embeddings
python -c "from embeddings import get_embedding; print('Embedding:', len(get_embedding('test')) if get_embedding('test') else 'Error')"

# Probar procesamiento PDF
python -c "from pdfs import pdf_to_text, chunk_text; texto = pdf_to_text('viajes_demo.pdf'); chunks = chunk_text(texto); print(f'Chunks: {len(chunks)}')"

# Verificar campos disponibles
python verificar_campos.py

# Probar búsqueda
python test_search.py

# Probar embeddings completos
python probar_embeddings.py
```

---

## 🎯 **SECUENCIA TÍPICA DE USO DIARIO**

### **Primera vez (setup completo)**
```bash
1. ollama serve
2. docker-compose up -d
3. python main.py
4. python chat_interactivo.py
```

### **Uso normal (ya configurado)**
```bash
1. ollama serve
2. docker-compose up -d
3. python chat_interactivo.py
```

### **Solo diagnóstico**
```bash
python diagnostico.py
```

---

## ⏰ **TIEMPOS ESTIMADOS**

| Comando | Tiempo Estimado |
|---------|----------------|
| `pip install ...` | 1-2 minutos |
| `ollama pull llama3.1` | 5-10 minutos |
| `docker-compose up -d` | 30-60 segundos |
| `python main.py` | 2-5 minutos |
| `python chat_interactivo.py` | Inmediato |
| Respuesta en chat | 10-30 segundos |

---

## 💡 **TIPS IMPORTANTES**

1. **Siempre ejecuta `ollama serve` ANTES que `main.py`**
2. **Mantén cada servicio en un terminal separado**
3. **Espera que Docker termine de iniciar antes de ejecutar scripts**
4. **Usa `diagnostico.py` si algo no funciona**
5. **El chat se cierra con `"salir"`**

---

## 📝 **ORDEN DE TERMINALES RECOMENDADO**

```
Terminal 1: ollama serve
Terminal 2: docker-compose up -d
Terminal 3: python main.py (solo primera vez)
Terminal 4: python chat_interactivo.py
```

---

*Comandos recopilados para el proyecto Weaviable - Sistema RAG*  
*Fecha: 30 de septiembre, 2025*