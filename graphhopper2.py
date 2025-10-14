import requests
import urllib.parse
import sys


ruta_url = "https://graphhopper.com/api/1/route?"

clave = "1a437f48-7e62-490c-99d9-2aa4e26b7e0f"

def geocodificacion(ubicacion, clave_api):
    """
    Esta función toma una ubicación (texto) y la clave de API,
    y devuelve el estado de la solicitud, latitud, longitud y el nombre formateado de la ubicación.
    """
    while not ubicacion:
        ubicacion = input("Por favor, ingrese una ubicación: ")
        if ubicacion.lower() in ["salir", "s"]:
            print("Saliendo del programa.")
            sys.exit()

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": clave_api})

    try:
        respuesta_datos = requests.get(url)
        datos_json = respuesta_datos.json()
        estado_json = respuesta_datos.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return 400, "null", "null", ubicacion

    if estado_json == 200 and len(datos_json.get("hits", [])) != 0:
        resultado = datos_json["hits"][0]
        lat = resultado["point"]["lat"]
        lng = resultado["point"]["lng"]
        nombre = resultado.get("name", "")
        valor = resultado.get("osm_value", "")
        pais = resultado.get("country", "")
        estado = resultado.get("state", "")

        if estado and pais:
            nueva_ubicacion = f"{nombre}, {estado}, {pais}"
        elif pais:
            nueva_ubicacion = f"{nombre}, {pais}"
        else:
            nueva_ubicacion = nombre

        print(f"URL de Geocodificación para {nueva_ubicacion} (Tipo: {valor}):\n{url}")
        return estado_json, lat, lng, nueva_ubicacion
    else:
        mensaje_error = datos_json.get("message", "No se encontró la ubicación o hubo un error.")
        print(f"Estado de la API de Geocodificación: {estado_json}\nMensaje de error: {mensaje_error}")
        return estado_json, "null", "null", ubicacion

# Bucle principal de la aplicación
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("auto, bicicleta, a pie")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    perfiles = ["auto", "bicicleta", "a pie"]
    vehiculo_seleccionado = input("Ingrese un perfil de vehículo de la lista (o 's' para salir): ")
    if vehiculo_seleccionado.lower() in ["salir", "s"]:
        break
    elif vehiculo_seleccionado not in perfiles:
        vehiculo_seleccionado = "auto"
        print("No se ingresó un perfil válido. Se usará 'auto' por defecto.")
    
    # Mapeo de español a inglés para la API
    vehiculo_api = {"auto": "car", "bicicleta": "bike", "a pie": "foot"}.get(vehiculo_seleccionado)

    ubicacion_inicio = input("Ubicación de inicio: ")
    if ubicacion_inicio.lower() in ["salir", "s"]:
        break
    origen = geocodificacion(ubicacion_inicio, clave)

    ubicacion_destino = input("Destino: ")
    if ubicacion_destino.lower() in ["salir", "s"]:
        break
    destino = geocodificacion(ubicacion_destino, clave)

    print("=================================================")
    if origen[0] == 200 and destino[0] == 200:
        op = f"&point={origen[1]}%2C{origen[2]}"
        dp = f"&point={destino[1]}%2C{destino[2]}"
        url_rutas = ruta_url + urllib.parse.urlencode({"key": clave, "vehicle": vehiculo_api, "locale": "es"}) + op + dp

        try:
            respuesta_rutas = requests.get(url_rutas)
            estado_rutas = respuesta_rutas.status_code
            datos_rutas = respuesta_rutas.json()
            
            print(f"Estado de la API de Rutas: {estado_rutas}\nURL de la API de Rutas:\n{url_rutas}")
            print("=================================================")

            if estado_rutas == 200:
                distancia_km = datos_rutas["paths"][0]["distance"] / 1000
                distancia_millas = distancia_km / 1.60934
                
                milisegundos = datos_rutas["paths"][0]["time"]
                segundos_totales = milisegundos // 1000
                horas = segundos_totales // 3600
                minutos = (segundos_totales % 3600) // 60
                segundos = segundos_totales % 60
                
                print(f"Indicaciones desde {origen[3]} hasta {destino[3]} en {vehiculo_seleccionado}")
                print("=================================================")
                print(f"Distancia recorrida: {distancia_millas:.2f} millas / {distancia_km:.2f} km")
                print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
                print("=============================================")

                for instruccion in datos_rutas["paths"][0]["instructions"]:
                    trayecto = instruccion["text"]
                    distancia_trayecto_km = instruccion["distance"] / 1000
                    millas_trayecto = distancia_trayecto_km / 1.60934
                    print(f"{trayecto} ( {distancia_trayecto_km:.2f} km / {millas_trayecto:.2f} millas )")
                print("=============================================")
            else:
                print(f"Mensaje de error: {datos_rutas.get('message', 'Error desconocido')}")
                print("*************************************************")
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión al solicitar la ruta: {e}")