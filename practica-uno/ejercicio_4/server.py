
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class Paciente:
    def __init__(self, CI, nombre, apellido, edad, genero, diagnostico, doctor):
        self.CI = CI
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.genero = genero
        self.diagnostico = diagnostico
        self.doctor = doctor

class PacienteBuilder:
    def __init__(self):
        self.data = {}

    def set_CI(self, CI):
        self.data["CI"] = CI
        return self

    def set_nombre(self, nombre):
        self.data["nombre"] = nombre
        return self

    def set_apellido(self, apellido):
        self.data["apellido"] = apellido
        return self

    def set_edad(self, edad):
        self.data["edad"] = edad
        return self

    def set_genero(self, genero):
        self.data["genero"] = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.data["diagnostico"] = diagnostico
        return self

    def set_doctor(self, doctor):
        self.data["doctor"] = doctor
        return self

    def build(self):
        return Paciente(**self.data)

class HospitalService:
    pacientes = []

    @staticmethod
    def add_paciente(paciente):
        HospitalService.pacientes.append(paciente)
        return paciente

    @staticmethod
    def find_paciente(ci):
        return next((paciente for paciente in HospitalService.pacientes if paciente.CI == ci), None)

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [paciente for paciente in HospitalService.pacientes if paciente.diagnostico == diagnostico]

    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [paciente for paciente in HospitalService.pacientes if paciente.doctor == doctor]

    @staticmethod
    def update_paciente(ci, data):
        paciente = HospitalService.find_paciente(ci)
        if paciente:
            for key, value in data.items():
                setattr(paciente, key, value)
            return paciente
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        paciente = HospitalService.find_paciente(ci)
        if paciente:
            HospitalService.pacientes.remove(paciente)
            return paciente
        else:
            return None

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "ci" in query_params:
                ci = int(query_params["ci"][0])
                paciente = HospitalService.find_paciente(ci)
                if paciente:
                    HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__])
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes = HospitalService.filter_pacientes_by_diagnostico(diagnostico)
                HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__ for paciente in pacientes])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes = HospitalService.filter_pacientes_by_doctor(doctor)
                HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__ for paciente in pacientes])
            else:
                HTTPResponseHandler.handle_response(self, 200, [paciente.__dict__ for paciente in HospitalService.pacientes])
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            paciente = PacienteBuilder().set_CI(data["CI"]).set_nombre(data["nombre"]).set_apellido(data["apellido"]).set_edad(data["edad"]).set_genero(data["genero"]).set_diagnostico(data["diagnostico"]).set_doctor(data["doctor"]).build()
            paciente = HospitalService.add_paciente(paciente)
            HTTPResponseHandler.handle_response(self, 201, paciente.__dict__)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            paciente = HospitalService.update_paciente(ci, data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = HospitalService.delete_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente.__dict__)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
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
