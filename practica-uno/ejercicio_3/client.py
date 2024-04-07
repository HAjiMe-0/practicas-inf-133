
import requests

url = "http://localhost:8000/pacientes"

# Crear un paciente
nuevo_paciente = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 35,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Pérez"
}
post_response_paciente = requests.post(url, json=nuevo_paciente)
print(post_response_paciente.text)

# Listar todos los pacientes
get_response_pacientes = requests.get(url)
print(get_response_pacientes.text)

# Buscar paciente por CI
ci_paciente = 1
get_response_paciente_ci = requests.get(f"{url}/{ci_paciente}")
print(get_response_paciente_ci.text)

# Listar pacientes por diagnóstico
diagnostico = "Diabetes"
get_response_pacientes_diagnostico = requests.get(f"{url}?diagnostico={diagnostico}")
print(get_response_pacientes_diagnostico.text)

# Listar pacientes por doctor
doctor = "Pedro Pérez"
get_response_pacientes_doctor = requests.get(f"{url}?doctor={doctor}")
print(get_response_pacientes_doctor.text)

# Actualizar información de un paciente
ci_paciente_actualizar = 1
nuevos_datos_paciente = {
    "nombre": "Juanito",
    "edad": 40
}
put_response_paciente = requests.put(f"{url}/{ci_paciente_actualizar}", json=nuevos_datos_paciente)
print(put_response_paciente.text)

# Eliminar un paciente
delete_response_paciente = requests.delete(f"{url}/{ci_paciente_actualizar}")
print(delete_response_paciente.text)
