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

# Ejemplo de uso
if __name__ == "__main__":
    client = get_weaviate_client()
    validate_connection(client)
    client.close()

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
