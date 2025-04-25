from datetime import datetime, date
from abc import ABC, abstractmethod


class Asiento:
    def __init__(self, numero: int, ocupado: bool = False):
        self.numero = numero
        self.ocupado = ocupado
    def obtenerNumero(self):
        return self.numero
    def verificarOcupacion(self)->bool:
        return self.ocupado
    def cambiarEstado(self):
        self.ocupado = not self.ocupado

class Unidad:
    def __init__(self, patente: str):
        self.patente = patente
        self.asientos: list[Asiento] = [Asiento(i) for i in range(1, 51)] # genera lista con 50 asientos desocupados (list comprehension)
    def obtenerAsientosLibres(self)->list[Asiento]:
        return [asiento for asiento in self.asientos if not asiento.verificarOcupacion()] #genera una lista con los asientos libres  (list comprehension)
    def verificarAsientoLibre(self, nroAsiento:int)->bool:
        return not self.asientos[nroAsiento -1].verificarOcupacion()
    def cambiarEstadoAsiento(self,nroAsiento:int):
        self.asientos[nroAsiento - 1].cambiarEstado()


class Ciudad:
    def __init__(self, codigo: str, nombre: str, provincia: str):
        self.codigo = codigo 
        self.nombre = nombre 
        self.provincia = provincia 

class Itinerario:
    def __init__(self, paradas:list[Ciudad]= []):
        self.paradas = paradas

class Pasajero:
    def __init__(self, nombre: str, email: str, dni: int):
        self.nombre = nombre
        self.email = email
        self.dni = dni
   
class Reserva:
    def __init__(self, fechaHora: datetime, asiento: Asiento, pasajero:Pasajero):
        self.fechaHora = fechaHora
        self.asiento = asiento
        self.pasajero = pasajero
    #consultas
    def obtenerAsientoNumero(self):
        return self.asiento.obtenerNumero()
    def obtenerFecha(self):
        return self.fechaHora


class Venta: 
    def __init__(self, fechaHora: datetime, asiento: Asiento):
        self.fechaHora = fechaHora
        self.asiento = asiento


class Servicio:
    def __init__(self, unidad: Unidad, calidad: str, precio: float, itinerario: Itinerario):
        self.unidad = unidad
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario
        self.ventas: list[Venta] = []
        self.reservas: list[Reserva] = []
#Asignaciones
    def asignarUnidad(self, unidad:Unidad):
        self.unidad= unidad
    def asignarItinerario(self, itinerario: Itinerario):
        self.itinerario = itinerario
#Inserciones
    def agregarReserva(self, reserva: Reserva) -> bool:
        if not self.unidad.verificarAsientoLibre(reserva.obtenerAsientoNumero()):
            raise ValueError("El asiento ya está ocupado.")
        if reserva in self.reservas:
            raise ValueError("La reserva ya existe.")
        self.reservas.append(reserva)
        self.unidad.cambiarEstadoAsiento(reserva.obtenerAsientoNumero())
        return True
#liberacion de reservas (se llama 30 min antes del viaje):
    def liberarAsientosReservados(self):
        for reserva in self.reservas:
            i = reserva.obtenerAsientoNumero()
            self.unidad.cambiarEstadoAsiento(i)
        self.reservas.clear()
#Consultas
    def obtenerAsientosLibres(self):
        return self.unidad.obtenerAsientosLibres()
    
############################################### MEDIOS DE PAGO  ###############################
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
    
################################################ CLASE SISTEMA ################################

class ArgenTUR:
    def __init__(self):
        self.sistemaActivo = True
