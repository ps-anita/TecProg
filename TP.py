from datetime import datetime, date
from abc import ABC, abstractmethod

class ArgenTUR:
    def __init__(self):
        self.sistemaActivo = True
        self.servicios = []
        self.reservas = []
        self.ventas = []
        self.unidades = []
        self.itinerarios = []
    def buscarServicio(self, servicio):
        for s in self.servicios:
            if(s==servicio):
                return s
        raise ValueError("Servicio no encontrado.")
    def consultarServiciosDisponibles(self):
        pass
    def agregarServicio(self, servicio):
        self.servicios.append(servicio)
    def asignarUnidad(self, servicio, unidad):
        try:
            s = self.buscarServicio(servicio)
            self.unidades.append(s.verUnidad())
        except ValueError:
            print("Servicio no encontrado.")
    def agregarItinerario(self, servicio, itinerario):
        try:
            s = self.buscarServicio(servicio)
            self.itinerarios.append(s.verItinerario())
        except ValueError:
            print("Servicio no encontrado.")
    def reservarPasaje(self, servicio, reserva):
        

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
    def __init__(self, nombre: str, email: str, dni: int):
        self.nombre = nombre
        self.email = email
        self.dni = dni

class Asiento:
    def __init__(self, numero: int, ocupado: bool):
        self.numero = numero
        self.ocupado = ocupado

class Venta: 
    def __init__(self, fechaHora: datetime):
        self.fechaHora = fechaHora

# interfaz 
class MedioPago(ABC):
    
    @abstractmethod
    def validarPago(self):
        pass

class TarjetaCredito(MedioPago):
    def __init__(self, numero: str, DNItitular: int, nombre: str, fechaVencimiento: date):
        self.numero = numero
        self.DNItitular = DNItitular
        self.nombre = nombre
        self.fechaVencimiento = date

    def validarPago(self):
        return True 

class MercadoPago(MedioPago):
    def __init__(self, celular: str, email: str):
        self.celular = celular
        self.email = email

    def validarPago(self):
        return True
    
class Uala(MedioPago):
    def __init__(self, email: str, nombreTitular: str):
        self.email = email
        self.nombreTitular = nombreTitular

    def validarPago(self):
        return True
    

