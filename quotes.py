import requests

def obtener_frase():
    # Usaremos esta API que es más estable
    url = "https://dummyjson.com/quotes/random"

    try:
        # 1. Hacemos la petición
        response = requests.get(url)
        
        # 2. Verificamos si hubo error
        response.raise_for_status()

        # 3. Convertimos la respuesta JSON a un Diccionario Python
        datos = response.json()

        # 4. Extraemos lo que nos interesa (según la documentación de DummyJSON)
        frase = datos["quote"]
        autor = datos["author"]

        # 5. Imprimimos bonito
        print("🌟 Frase del día:")
        print(f'"{frase}"')
        print(f"   — {autor}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except KeyError:
        print("❌ Error: La API cambió el formato de los datos.")

if __name__ == "__main__":
    obtener_frase()