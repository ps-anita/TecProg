from datetime import datetime, date
from abc import ABC, abstractmethod
import random

class ArgenTUR:
    def __init__(self):
        self.sistemaActivo = True

class Unidad:
    def __init__(self, patente: str):
        self.patente = patente

class Ciudad:
    def __init__(self, codigo: str, nombre: str, provincia: str):
        self.codigo = codigo 
        self.nombre = nombre 
        self.provincia = provincia 

class Itinerario:
    def __init__(self):
        self.paradas = []

class Servicio:
    def __init__(self, unidad: Unidad, calidad: str, precio: int, itinerario: Itinerario):
        self.unidad = unidad
        self.calidad = calidad
        self.precio = precio
        self.itineriario = itinerario

class Reserva:
    def __init__(self, fechaHora: datetime):
        self.fechaHora = fechaHora

class Pasajero:
    def __init__(self, nombre: str, apellido: str email: str, dni: int):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
    def obtener_nombre(self): return self.nombre
    def obtener_dni(self): return self.dni
    def obtener_email(self): return self.email
    def obtener_apellido(self): return self.apellido

class Asiento:
    def __init__(self, numero: int, ocupado: bool):
        self.numero = numero
        self.ocupado = ocupado

# Interfaz 
class MedioPago(ABC):
    @abstractmethod
    def validarPago(self):
        pass
    @abstractmethod
    def obtener_datos_pago(self):
        pass

class TarjetaCredito(MedioPago):
    def __init__(self, numero: str, dni_t: int, nombre_pasajero: str, f_vencimiento: date):
        self.nombre_metodo="Tarjeta de Crédito"
        self.numero = numero
        self.dni_titular = dni_t
        self.nombre_pasajero = nombre_pasajero
        self.fecha_vencimiento = f_vencimiento
        self.servicio_externo=ServicioExternoPago(self)
    def validarPago(self):
        return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self):
        return f"{self.nombre_metodo} - Nombre Titular {self.nombre_pasajero} - DNI {self.dni_titular} - Número Tarjeta {self.numero} - Vencimiento {self.fecha_vencimiento.day}/{self.fecha_vencimiento.month}/{self.fecha_vencimiento.year}"
   
class MercadoPago(MedioPago):
    def __init__(self, celular: str, email: str):
        self.nombre_metodo="Mercado Pago"
        self.celular = celular
        self.email = email
        self.servicio_externo=ServicioExternoPago(self)
    def validarPago(self):
        return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self):
        return f"{self.nombre_metodo} - Celular {self.celular} - Email {self.email}"

class Uala(MedioPago):
    def __init__(self, email: str, nombre_t: str):
        self.nombre_metodo="Ualá"
        self.email = email
        self.nombre_titular = nombre_t
        self.servicio_externo=ServicioExternoPago(self)
    def validarPago(self):
        return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self):
        return f"{self.nombre_metodo} - NombreTitular {self.nombre_titular} - Email {self.email}"
    
class ServicioExternoPago:
    def __init__(self, m_pago:MedioPago):
        self.medio_pago=m_pago
    def verificar_pago(self)->bool:
        return random.choice([True,False,True])

class Venta: 
    def __init__(self, _fecha_Hora: datetime, a_asiento: Asiento, s_servicio: Servicio, p_pasajero: Pasajero, m_pago: MedioPago):
        self.fecha_hora = _fecha_Hora
        self.asiento = a_asiento
        self.servicio= s_servicio
        self.pasajero= p_pasajero
        self.medio_pago= m_pago
        self.concretada= False
    def verificar_pago_valido(self):            #Se fija si el medio de pago es válido
        return self.medio_pago.validarPago()
    def concretar_venta(self):
        if self.verificar_pago_valido(): self.concretada= True
    def obtener_registro_venta(self):
        print(f"Registro de Venta - {self.fecha_hora.day}/{self.fecha_hora.month}/{self.fecha_hora.year} {self.fecha_hora.strftime('%H:%M:%S')}")
        print(f"- Datos Pasajero: {self.pasajero.obtener_nombre()} - DNI {self.pasajero.obtener_dni()}")
        print(f"- Asiento Reservado: {self.asiento.obtenerNumero()}")
        print(f"- Medio de Pago: {self.medio_pago.obtener_datos_pago()}")
