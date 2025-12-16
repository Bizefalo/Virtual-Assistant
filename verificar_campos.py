from clusteConection import get_weaviate_client

def verificar_datos_disponibles():
    client = get_weaviate_client()
    collection = client.collections.get('Viaje')
    
    # Ver qué campos/propiedades tenemos
    results = collection.query.fetch_objects(limit=1)
    
    if results.objects:
        obj = results.objects[0]
        print("🔍 **CAMPOS DISPONIBLES EN LOS DATOS:**")
        print("="*50)
        
        for campo, valor in obj.properties.items():
            print(f"✅ {campo}: {valor}")
            
        print("\n❌ **CAMPOS NO DISPONIBLES:**")
        campos_faltantes = ['precio', 'costo', 'presupuesto', 'valor', 'tarifa']
        for campo in campos_faltantes:
            print(f"❌ {campo}")
    
    client.close()

if __name__ == "__main__":
    verificar_datos_disponibles()