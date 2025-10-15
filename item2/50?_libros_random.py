import requests
import json
import random
from faker import Faker     # Randomizador de datos (titulos, nombres, apellidos...) #

# --- CONFIGURACIÓN DE API --- #
URL_API = "http://library.demo.local/api/v1/books"
TOKEN_API = "cisco|jXbn26bBkPYfSEH5lWSnkmKWxEfpJO9qWJ-EXYILQbw"
fake = Faker()              # Se llama la libreria faker para iniciarlo #

# Metodo de comunicacion de la API + Verificacion de token confiable #
post_headers = {
    "Content-Type": "application/json",
    "X-API-Key": TOKEN_API              # IMPORTANTE: Si no funciona probablemente se debe actualizar el token #
}



# Proceso de script para generar X cantidad de libros #
def gen_random_libros():
    print("--- Generando libros aleatorios... ---")
    libros_creados_con_exito = 0

    # Bucle for para repetir el proceso de creación 50 veces #
    for i in range(50):             # range(X) = repeticion de proceso X veces #
                                    # Formato de creacion de libro de la API #
        libro_nuevo = {
            "id":       random.randint(100, 99999),                 # sE elige un numero random entre 100 y 99999 #
            "title":    fake.sentence(nb_words=4).replace('.', ''), # Uso de funcion de libreria faker. nb_word establece el maximo de palabras que usa el titulo#
            "author":   fake.name(),                                # Se genera una identidad aleatoria con fake.name() #
            "isbn":     fake.isbn13()                               # Se genera un ISBN random de 13 numeros #
        }

        try:
            # Se usa 'requests.post' para enviar datos y crear un nuevo recurso en la API #
            # 'json.dumps()' convierte el diccionario de Python a un string en formato JSOn #
            response = requests.post(URL_API, headers=post_headers, data=json.dumps(libro_nuevo), timeout=10)
            
            # Los códigos 200 o 201 indican que el libro se agregó con éxito #
            if response.status_code in [200, 201]:
                respuesta_json = response.json()
                if respuesta_json.get("title") is not None:
                    print(f"Libro {i+1}/50 agregado con exito: '{libro_nuevo['title']}'")
                    libros_creados_con_exito += 1
                else:
                    print(f"Libro {i+1}/50 -> La API devolvió datos nulos (Error del servidor).")
            else:
                print(f"Error al agregar el libro {i+1}: Codigo {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Error de conexion al agregar el libro {i+1}: {e}")
            
    print(f"\n--- Proceso finalizado. Total de libros creados: {libros_creados_con_exito} ---")

#   Ejecucion del script    #
if __name__ == "__main__":
    gen_random_libros()