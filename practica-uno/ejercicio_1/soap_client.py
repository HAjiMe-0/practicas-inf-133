from zeep import Client

client = Client('http://localhost:8000')
suma = client.service.Sumar(num1=115, num2=90)
resta = client.service.Restar(num1=124, num2=546)
multiplicacion = client.service.Multiplicar(num1=7, num2=100)
division = client.service.Dividir(num1=80, num2=8)

print(suma)
print(resta)
print(multiplicacion)
print(division)