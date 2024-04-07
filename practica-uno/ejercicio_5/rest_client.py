import requests

base_url = "http://localhost:8000"

# Función para realizar una solicitud GET y mostrar la respuesta
def get_request(endpoint):
    response = requests.get(base_url + endpoint)
    print(response.status_code)
    print(response.text)

# Función para realizar una solicitud POST y mostrar la respuesta
def post_request(endpoint, data):
    response = requests.post(base_url + endpoint, json=data)
    print(response.status_code)
    print(response.text)

# Función para realizar una solicitud PUT y mostrar la respuesta
def put_request(endpoint, id, data):
    response = requests.put(base_url + endpoint + f"/{id}", json=data)
    print(response.status_code)
    print(response.text)

# Función para realizar una solicitud DELETE y mostrar la respuesta
def delete_request(endpoint, id):
    response = requests.delete(base_url + endpoint + f"/{id}")
    print(response.status_code)
    print(response.text)

# Crear un nuevo animal
nuevo_animal = {
    "nombre": "León",
    "especie": "Panthera leo",
    "genero": "Masculino",
    "edad": 5,
    "peso": 180
}
post_request("/animales", nuevo_animal)

# Listar todos los animales
get_request("/animales")

# Buscar animales por especie
get_request("/animales?especie=Panthera leo")

# Buscar animales por género
get_request("/animales?genero=Masculino")

# Actualizar información de un animal
animal_id = 1  
datos_actualizados = {
    "nombre": "León Rey",
    "edad": 6
}
put_request("/animales", animal_id, datos_actualizados)

# Eliminar un animal
animal_id_a_eliminar = 1  
delete_request("/animales", animal_id_a_eliminar)
