from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Animal:
    def __init__(self, nombre, especie, genero, edad, peso):
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

    def emitir_sonido(self):
        pass

class Mamifero(Animal):
    def emitir_sonido(self):
        return "Sonido de mamífero"

class Ave(Animal):
    def emitir_sonido(self):
        return "Sonido de ave"

class Reptil(Animal):
    def emitir_sonido(self):
        return "Sonido de reptil"

class Anfibio(Animal):
    def emitir_sonido(self):
        return "Sonido de anfibio"

class Pez(Animal):
    def emitir_sonido(self):
        return "Sonido de pez"

class AnimalFactory:
    @staticmethod
    def create_animal(tipo, nombre, especie, genero, edad, peso):
        if tipo == "Mamífero":
            return Mamifero(nombre, especie, genero, edad, peso)
        elif tipo == "Ave":
            return Ave(nombre, especie, genero, edad, peso)
        elif tipo == "Reptil":
            return Reptil(nombre, especie, genero, edad, peso)
        elif tipo == "Anfibio":
            return Anfibio(nombre, especie, genero, edad, peso)
        elif tipo == "Pez":
            return Pez(nombre, especie, genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")

class AnimalService:
    animales = []

    @staticmethod
    def crear_animal(data):
        animal = AnimalFactory.create_animal(data["tipo"], data["nombre"], data["especie"], data["genero"], data["edad"], data["peso"])
        animal.id = len(AnimalService.animales) + 1
        AnimalService.animales.append(animal.__dict__)
        return animal.__dict__

    @staticmethod
    def listar_animales():
        return AnimalService.animales

    @staticmethod
    def buscar_animales_por_especie(especie):
        return [animal for animal in AnimalService.animales if animal["especie"] == especie]

    @staticmethod
    def buscar_animales_por_genero(genero):
        return [animal for animal in AnimalService.animales if animal["genero"] == genero]

    @staticmethod
    def actualizar_informacion_animal(id, data):
        for animal in AnimalService.animales:
            if animal["id"] == id:
                animal.update(data)
                return animal
        return None

    @staticmethod
    def eliminar_animal(id):
        for animal in AnimalService.animales:
            if animal["id"] == id:
                AnimalService.animales.remove(animal)
                return animal
        return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animal = AnimalService.crear_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animal)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            especie = query_params.get("especie", None)
            genero = query_params.get("genero", None)
            if especie:
                animales = AnimalService.buscar_animales_por_especie(especie[0])
                HTTPResponseHandler.handle_response(self, 200, animales)
            elif genero:
                animales = AnimalService.buscar_animales_por_genero(genero[0])
                HTTPResponseHandler.handle_response(self, 200, animales)
            else:
                animales = AnimalService.listar_animales()
                HTTPResponseHandler.handle_response(self, 200, animales)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = self.read_data()
            animal = AnimalService.actualizar_informacion_animal(animal_id, data)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            animal = AnimalService.eliminar_animal(animal_id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
