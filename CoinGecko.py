import requests
import pandas as pd
import time

# URL base de la API de CoinGecko
url_gecko = 'https://api.coingecko.com/api/v3/coins/markets'

# Categorías a consultar
categorias = [ 'real-world-assets-rwa', 'meme-token','artificial-intelligence', 'gaming']

# Lista para almacenar los datos
datos_proyectos = []

# Función para obtener los datos de cada categoría
def obtener_datos_categoria(categoria):
    page = 1
    while True:
        params = {
            'vs_currency': 'usd',
            'category': categoria,
            'order': 'market_cap_desc',
            'per_page': 250,  # CoinGecko permite obtener hasta 250 proyectos por página
            'page': page
        }
        
        response = requests.get(url_gecko, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                break  # Si no hay más datos, salir del bucle
            for crypto in data:
                # Extraer los datos relevantes y agregar la categoría
                datos_proyectos.append({
                    'id': crypto['id'],
                    'name': crypto['name'],
                    'symbol': crypto['symbol'],
                    'circulating_supply': crypto.get('circulating_supply'),
                    'total_supply': crypto.get('total_supply'),
                    'max_supply': crypto.get('max_supply'),
                    'cmc_rank': crypto.get('market_cap_rank'),
                    'price': crypto.get('current_price'),
                    'market_cap': crypto.get('market_cap'),
                    'volume_24h': crypto.get('total_volume'),
                    'category': categoria
                })
            page += 1
        elif response.status_code == 429:
            print(f"Error 429: Límite de solicitudes alcanzado. Esperando 60 segundos antes de reintentar la categoría {categoria}...")
            time.sleep(60)
        else:
            print(f"Error {response.status_code} al obtener la categoría {categoria}")
            break

# Obtener los datos de cada categoría
for categoria in categorias:
    print(f"Obteniendo datos para la categoría: {categoria}")
    obtener_datos_categoria(categoria)

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(datos_proyectos)

# Guardar los datos en un archivo CSV
df.to_csv('proyectos_criptos_categorias_meow.csv', index=False)

print("Datos guardados en 'proyectos_criptos_categorias123.csv'")

