import requests

def consultar_plantas():
    url = 'http://localhost:8000/graphql'
    query = """
    {
        plantas {
            id
            nombreComun
            especie
            edad
            altura
            tieneFrutosSSS
        }
    }
    """
    response = requests.post(url, json={'query': query})
    return response.json()

def buscar_plantas_por_especie(especie):
    url = 'http://localhost:8000/graphql'
    query = """
    {
        plantasPorEspecie(especie: "%s") {
            id
            nombreComun
            especie
            edad
            altura
            tieneFrutos
        }
    }
    """ % especie
    response = requests.post(url, json={'query': query})
    return response.json()

def buscar_plantas_con_frutos():
    url = 'http://localhost:8000/graphql'
    query = """
    {
        plantasConFrutos {
            id
            nombreComun
            especie
            edad
            altura
            tieneFrutos
        }
    }
    """
    response = requests.post(url, json={'query': query})
    return response.json()

def crear_planta(nombre_comun, especie, edad, altura, tiene_frutos):
    url = 'http://localhost:8000/graphql'
    query = """
    mutation {
        crearPlanta(nombreComun: "%s", especie: "%s", edad: %d, altura: %d, tieneFrutos: %s) {
            planta {
                id
                nombreComun
                especie
                edad
                altura
                tieneFrutos
            }
        }
    }
    """ % (nombre_comun, especie, edad, altura, str(tiene_frutos).lower())
    response = requests.post(url, json={'query': query})
    return response.json()

def actualizar_planta(id, nombre_comun, especie, edad, altura, tiene_frutos):
    url = 'http://localhost:8000/graphql'
    query = """
    mutation {
        actualizarPlanta(id: %d, nombreComun: "%s", especie: "%s", edad: %d, altura: %d, tieneFrutos: %s) {
            planta {
                id
                nombreComun
                especie
                edad
                altura
                tieneFrutos
            }
        }
    }
    """ % (id, nombre_comun, especie, edad, altura, str(tiene_frutos).lower())
    response = requests.post(url, json={'query': query})
    return response.json()

def eliminar_planta(id):
    url = 'http://localhost:8000/graphql'
    query = """
    mutation {
        eliminarPlanta(id: %d) {
            planta {
                id
                nombreComun
                especie
                edad
                altura
                tieneFrutos
            }
        }
    }
    """ % id
    response = requests.post(url, json={'query': query})
    return response.json()

if __name__ == "__main__":
    # Ejemplo de uso
    print("Consultar todas las plantas:")
    print(consultar_plantas())

    print("\nBuscar plantas por especie (Rosa):")
    print(buscar_plantas_por_especie("Rosa"))

    print("\nBuscar plantas con frutos:")
    print(buscar_plantas_con_frutos())

    print("\nCrear una nueva planta:")
    print(crear_planta("Naranjo", "Citrus sinensis", 24, 150, True))

    print("\nActualizar la información de una planta:")
    print(actualizar_planta(1, "Rosa mosqueta", "Rosa canina", 36, 50, True))

    print("\nEliminar una planta:")
    print(eliminar_planta(2))
