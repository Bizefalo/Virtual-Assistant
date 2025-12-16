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