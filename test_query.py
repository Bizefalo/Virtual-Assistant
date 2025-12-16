from clusteConection import get_weaviate_client

client = get_weaviate_client()
collection = client.collections.get('Viaje')

# Ver todos los objetos almacenados
results = collection.query.fetch_objects(limit=10)

print('=== DATOS EN WEAVIATE ===')
print(f'Total objetos encontrados: {len(results.objects)}')

for i, obj in enumerate(results.objects):
    print(f'\nObjeto {i+1}:')
    print(f'  - Destino: {obj.properties.get("destino", "N/A")}')
    print(f'  - Descripción: {obj.properties.get("descripcion", "N/A")[:100]}...')
    print(f'  - Rating: {obj.properties.get("rating", "N/A")}')

client.close()