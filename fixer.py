import requests as rq
from decimal import Decimal, ROUND_DOWN
from currencies import curr
from requests import get


class ManagerApi:
    def __init__(self):
        pass

    def obtener_moneda_cantidad(self):
        moneda_comprar = input("Ingrese la moneda que desea comprar: ").upper()
        cantidad_comprar = Decimal(input("Ingrese la cantidad de {} que desea comprar: ".format(moneda_comprar)))
        return moneda_comprar, cantidad_comprar

    def obtener_cotizacion(self, moneda_comprar):
        response = get("http://data.fixer.io/api/latest?access_key=61cba135acfff860e587148001f83a46&curr")
        res_json = response.json()
        cot_peso_moneda = Decimal(res_json['rates']['ARS']) / Decimal(res_json['rates'][moneda_comprar])
        return cot_peso_moneda

    def calcular_equivalente(self, moneda_comprar, cantidad_comprar, username):
        cot_peso_moneda = self.obtener_cotizacion(moneda_comprar)
        cantidad_peso = cantidad_comprar * cot_peso_moneda
        cantidad_peso = cantidad_peso.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        
    
        print("Calculo de Conversion Realizado.")
        
        return cantidad_peso


