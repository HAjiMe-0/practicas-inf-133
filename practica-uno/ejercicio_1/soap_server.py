from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

def sumar(num1, num2):
    result = num1 + num2
    return "La suma de {} + {} es {}".format(num1, num2, result)

def resta(num1, num2):
    result = num1 - num2
    return "La resta de {} - {} es {}".format(num1, num2, result)

def multiplicacion(num1, num2):
    result = num1 * num2
    return "La multiplicación de {} * {} es {}".format(num1, num2, result)

def division(num1, num2):
    result = num1 / num2
    return "La división de {} / {} es {}".format(num1, num2, nresult)

dispatcher = SoapDispatcher(
    'soap-server',
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"sumar": str},
    args={"num1": int, "num2": int},
)

dispatcher.register_function(
    "Restar",
    resta,
    returns={"resta": str},
    args={"num1": int, "num2": int},
)

dispatcher.register_function(
    "Multiplicar",
    multiplicacion,
    returns={"multiplicacion": str},
    args={"num1": int, "num2": int},
)

dispatcher.register_function(
    "Dividir",
    division,
    returns={"division": str},
    args={"num1": int, "num2": int},
)

server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()