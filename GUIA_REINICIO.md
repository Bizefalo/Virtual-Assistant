# 🔄 GUÍA DE REINICIO RÁPIDO - Sistema RAG

## 🚀 **REINICIO COMPLETO (Desde Cero)**

### Paso 1: Limpiar todo
```bash
# 1. Parar y eliminar contenedores Docker
docker-compose down
docker system prune -f

# 2. Limpiar datos de Weaviate (opcional - elimina todos los datos)
python limpiar_datos.py
```

### Paso 2: Reiniciar servicios
```bash
# 1. Terminal 1: Iniciar Ollama
ollama serve

# 2. Terminal 2: Levantar Weaviate
docker-compose up -d

# Verificar que ambos estén corriendo
docker-compose ps
ollama list
```

### Paso 3: Procesar datos nuevamente
```bash
# 3. Terminal 3: Ejecutar procesamiento completo
python main.py
```

### Paso 4: Usar el sistema
```bash
# 4. Terminal 4: Chat interactivo
python chat_interactivo.py
```

---

## ⚡ **REINICIO RÁPIDO (Solo Servicios)**

Si solo necesitas reiniciar los servicios pero mantener los datos:

```bash
# 1. Reiniciar Weaviate
docker-compose restart

# 2. Verificar Ollama (si sigue corriendo, no hagas nada)
# Si no está corriendo:
ollama serve

# 3. Probar directamente
python chat_interactivo.py
```

---

## 🔧 **REINICIO SELECTIVO**

### Solo reiniciar Weaviate:
```bash
docker-compose restart
```

### Solo reiniciar Ollama:
```bash
# Ctrl+C en la terminal de ollama serve, luego:
ollama serve
```

### Solo limpiar datos (mantener servicios):
```bash
python limpiar_datos.py
python main.py
```

---

## 🆘 **REINICIO DE EMERGENCIA**

Si algo está muy roto:

```bash
# 1. Matar todo
docker-compose down --volumes  # Elimina datos también
taskkill /f /im ollama.exe     # En Windows

# 2. Limpiar completamente
docker system prune -a -f
docker volume prune -f

# 3. Empezar desde cero
docker-compose up -d
ollama serve
python main.py
```

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

Antes de usar el sistema, verifica:

```bash
# ✅ Docker corriendo
docker-compose ps

# ✅ Ollama corriendo  
ollama list

# ✅ Conexión a Weaviate
python -c "from clusteConection import get_weaviate_client, validate_connection; client = get_weaviate_client(); validate_connection(client); client.close()"

# ✅ Datos en Weaviate
python -c "from clusteConection import get_weaviate_client; client = get_weaviate_client(); collection = client.collections.get('Viaje'); results = collection.query.fetch_objects(limit=1); print(f'Documentos: {len(results.objects)}'); client.close()"
```

---

## 📋 **COMANDOS RÁPIDOS**

### Iniciar todo (orden correcto):
```bash
# Terminal 1
ollama serve

# Terminal 2  
docker-compose up -d

# Terminal 3
python main.py

# Terminal 4
python chat_interactivo.py
```

### Parar todo:
```bash
# Ctrl+C en terminal de Ollama
# Luego:
docker-compose down
```

### Verificar estado:
```bash
docker-compose ps
ollama list
python diagnostico.py
```

---

## 🎯 **CASOS COMUNES**

### **Caso 1:** "Quiero empezar fresh con nuevos datos"
```bash
python limpiar_datos.py
# Cambiar el PDF o los metadatos en main.py si quieres
python main.py
python chat_interactivo.py
```

### **Caso 2:** "Los servicios están corriendo pero no responde"
```bash
docker-compose restart
# Esperar 30 segundos
python diagnostico.py
```

### **Caso 3:** "Error de conexión"
```bash
# Verificar puertos
netstat -an | findstr :8080   # Weaviate
netstat -an | findstr :11434  # Ollama

# Si alguno falta, reiniciar ese servicio
```

### **Caso 4:** "Quiero cambiar de modelo de Ollama"
```bash
# Descargar nuevo modelo
ollama pull llama3.2

# Cambiar en embeddings.py:
# Línea: json={'model': 'llama3.2', 'input': text}

# Limpiar y resubir datos
python limpiar_datos.py
python main.py
```

---

## ⏰ **TIEMPOS ESTIMADOS**

- **Reinicio completo**: 5-10 minutos
- **Reinicio rápido**: 1-2 minutos  
- **Solo limpiar datos**: 2-3 minutos
- **Verificaciones**: 30 segundos

---

## 💡 **TIPS IMPORTANTES**

1. **Siempre inicia Ollama ANTES que main.py** - main.py necesita que Ollama esté corriendo
2. **Espera que Docker termine de iniciar** - No corras main.py inmediatamente después de `docker-compose up -d`
3. **Un terminal por servicio** - Ollama en un terminal, chat en otro
4. **Usa diagnostico.py** - Para verificar que todo esté bien antes de usar el chat

---

## 🔍 **COMANDO SÚPER RÁPIDO**

Si quieres verificar todo de una vez:

```bash
python -c "
import subprocess
import time

print('🔍 Verificando servicios...')

# Docker
result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True)
print('Docker:', '✅' if 'weaviable-weaviate-1' in result.stdout else '❌')

# Ollama  
result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
print('Ollama:', '✅' if 'llama3.1' in result.stdout else '❌')

print('¡Listo para usar!')
"
```

---

**💡 Consejo:** Guarda estos comandos en un archivo .bat o .ps1 para ejecutarlos rápidamente en el futuro.