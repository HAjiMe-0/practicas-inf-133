
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class HospitalService:
    pacientes = []
    
    @staticmethod
    def crear_paciente(data):
        paciente = {
            "CI": data["CI"],
            "nombre": data["nombre"],
            "apellido": data["apellido"],
            "edad": data["edad"],
            "genero": data["genero"],
            "diagnostico": data["diagnostico"],
            "doctor": data["doctor"]
        }
        HospitalService.pacientes.append(paciente)
        return paciente

    @staticmethod
    def add_paciente(data):
        data["ci"] = len(HospitalService.pacientes) + 1
        HospitalService.pacientes.append(data)
        return data

    @staticmethod
    def find_paciente(ci):
        return next((paciente for paciente in HospitalService.pacientes if paciente["ci"] == ci), None)

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [paciente for paciente in HospitalService.pacientes if paciente["diagnostico"] == diagnostico]

    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [paciente for paciente in HospitalService.pacientes if paciente["doctor"] == doctor]

    @staticmethod
    def update_paciente(ci, data):
        paciente = HospitalService.find_paciente(ci)
        if paciente:
            paciente.update(data)
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
                    HTTPResponseHandler.handle_response(self, 200, [paciente])
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes = HospitalService.filter_pacientes_by_diagnostico(diagnostico)
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes = HospitalService.filter_pacientes_by_doctor(doctor)
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(self, 200, HospitalService.pacientes)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            paciente = HospitalService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, paciente)
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            paciente = HospitalService.update_paciente(ci, data)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Paciente no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = HospitalService.delete_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, paciente)
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
