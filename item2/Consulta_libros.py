import requests
import time

# --- CONFIGURACIÓN ---
URL_API = "http://library.demo.local/api/v1/books?includeISBN=true"     # URL de libros + ISBN incluido #
TOKEN_API = "cisco|VAWB2IvNIvDCK58fMnSpIit6B7o2VIoTmp5XQUkxa_E"

def listar_todos_los_libros():
    print("--- Iniciando consulta de todos los los libros en la biblioteca ---")
    
    # Solicitud GET #
    headers = {
        "X-API-Key": TOKEN_API      # IMPORTANTE: Mantener token actualizado #
    }
    
    
    todos_los_libros = []       # Lista que registrara los libros leidos #
    pagina_actual = 0           # Variable que establece la pagina inicial #
    
    # Bucle 'while' para manejar la paginación de la API (pedir página por página) #
    while True:

        # Parametro que permitira completar la URL de nuestra consulta #
        params = {
            "page": pagina_actual
        }
        
        # "Try" es basicamente pedirle al script que intente llevar a cabo lo que esta dentro de su string #
        try:
            print(f"Buscando libros en la página {pagina_actual}...")
            response = requests.get(URL_API, headers=headers, params=params, timeout=10) # Respuesta = solicitud GET a http://library.demo.local/api/v1/books?page=1&includeISBN=true 
            
            if response.status_code == 200:             # Si la consulta es valida, se crea una variable que contiene los datos de la solicitud GET. En este caso seria la informacion de los libros #
                libros_en_pagina = response.json()
                
                # Si hay datos en la variable antes creada, se almacena esa informacion en la lista vacia que registra los libros #
                if libros_en_pagina:
                    todos_los_libros.extend(libros_en_pagina)
                    pagina_actual += 1                          # Se suma +1 a la variable pagina actual para llevar a cabo nuevamente el bucle, pero con otra pagina
 
                # Si la pagina a la que se consulta no tiene datos, no se crea la variable, por lo que no hay mas libros que registrar. Se rompe el bucle #
                else:
                    print("Se han obtenido todos los libros.")
                    break
            else:
                print(f"Error al obtener la página {pagina_actual}. Código: {response.status_code}")
                break
        
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión. No se pudo completar la solicitud. Detalle: {e}")
            break

        # Pausa para no colapsar la API #
        time.sleep(2.5)

    print("\n--- Catálogo Completo de la Biblioteca ---")
    if todos_los_libros:
        print(f"Total de libros encontrados: {len(todos_los_libros)}")
        print("-------------------------------------------")
        for libro in todos_los_libros:
            libro_id = libro.get('id', 'N/A')
            titulo = libro.get('title', 'Sin Título')
            autor = libro.get('author', 'Autor Desconocido')
            isbn = libro.get('isbn', 'ISBN Desconocido')
            
            print(f"  - ID: {libro_id} | Título: {titulo} | Autor: {autor} | ISBN: {isbn} ")
    else:
        print("No se encontraron libros en la biblioteca o no se pudo acceder a la API.")

if __name__ == "__main__":
    listar_todos_los_libros()