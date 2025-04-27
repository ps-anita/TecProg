from datetime import datetime, date
from abc import ABC, abstractmethod
import random

class Asiento:
    def __init__(self, numero: int, libre: bool = True):
        self.numero = numero
        self.libre = libre
    def obtener_numero(self):
        return self.numero
    def verificar_libre(self)->bool:
        return self.libre
    def cambiar_estado(self):
        self.libre = not self.libre

class Unidad:
    def __init__(self, patente: str):
        self.patente = patente
        self.asientos: list[Asiento] = [Asiento(i) for i in range(1, 51)] # genera lista con 50 asientos desocupados (list comprehension)
    def obtener_asientos_libres(self)->list[Asiento]:
        return [asiento for asiento in self.asientos if asiento.verificar_libre()] #genera una lista con los asientos libres  (list comprehension)
    def verificar_asiento_libre(self, nro_asiento:int)->bool:
        return self.asientos[nro_asiento -1].verificar_libre()
    def cambiarEstadoAsiento(self,nro_asiento:int):
        self.asientos[nro_asiento - 1].cambiar_estado()

class Ciudad:
    def __init__(self, codigo: str, nombre: str, provincia: str):
        self.codigo = codigo 
        self.nombre = nombre 
        self.provincia = provincia 

class Itinerario:
    def __init__(self, paradas: list[Ciudad] = None):
        self.paradas = paradas if paradas is not None else []

class Pasajero:
    def __init__(self, nombre: str,apellido:str, email: str, dni: int):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
    def obtener_nombre(self): return self.nombre
    def obtener_dni(self): return self.dni
    def obtener_email(self): return self.email
    def obtener_apellido(self): return self.apellido
   
class Reserva:
    def __init__(self, fecha_hora: datetime, asiento: Asiento, pasajero:Pasajero):
        self.fecha_hora = fecha_hora
        self.asiento = asiento
        self.pasajero = pasajero
    #consultas
    def obtener_asiento_numero(self):
        return self.asiento.obtener_numero()
    def obtenerFecha(self):
        return self.fecha_hora

class Venta: 
    def __init__(self, fecha_hora: datetime, asiento: Asiento):
        self.fecha_hora = fecha_hora
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
    def asignar_unidad(self, unidad:Unidad):
        self.unidad= unidad
    def asignar_itinerario(self, itinerario: Itinerario):
        self.itinerario = itinerario
#Inserciones
    def agregar_reserva(self, reserva: Reserva) -> bool:
        nro_asiento = reserva.obtener_asiento_numero()
        if not self.unidad.verificar_asiento_libre(nro_asiento):
            raise ValueError("El asiento ya está ocupado.")
        self.reservas.append(reserva)
        self.unidad.cambiar_estado_asiento(nro_asiento)
        return True
#liberacion de reservas (se llama 30 min antes del viaje):
    def liberar_asientos_reservados(self):
        for reserva in self.reservas:
            i = reserva.obtener_asiento_numero()
            self.unidad.cambiar_estado_asiento(i)
        self.reservas.clear()
#Consultas
    def obtener_asientos_libres(self):
        return self.unidad.obtener_asientos_libres()
    
############################################### MEDIOS DE PAGO  ###############################
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
        return f"{self.nombre_metodo} - Nombre Titular {self.nombre_titular} - Email {self.email}"
    
class ServicioExternoPago:
    def __init__(self, m_pago:MedioPago):
        self.medio_pago=m_pago
    def verificar_pago(self)->bool:
        return random.choice([True,False,True])
    
################################################ CLASE SISTEMA ################################

class ArgentinaTur:
    def __init__(self):
        self.sistema_activo = True
