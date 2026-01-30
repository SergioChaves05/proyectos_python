import requests 
from bs4 import BeautifulSoup
import csv

response = requests.get("https://books.toscrape.com/")

# TRUCO PRO: Forzamos a Python a entender que la web está en UTF-8
# Esto suele arreglar el problema de raíz antes de leer nada
response.encoding = 'utf-8' 

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Title: {soup.title.text}")

    # Abrimos el archivo ANTES del bucle
    with open('libros.csv', mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['Titulo', 'Precio', 'Stock'])

        libros = soup.find_all('article', class_='product_pod')
        
        for libro in libros:
            titulo = libro.h3.a['title']
            
            # --- CORRECCIÓN AQUÍ ---
            precio_sucio = libro.find('p', class_='price_color').text
            # Reemplazamos la 'Â' por una cadena vacía (la borramos)
            precio = precio_sucio.replace('Â', '') 
            
            stock = libro.find('p', class_='instock availability').text.strip()
            
            print(f"Libro: {titulo}, Precio: {precio}, Stock: {stock}")
            escritor.writerow([titulo, precio, stock])

else:
    print("Error de conexión")