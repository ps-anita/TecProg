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
    def cambiar_estado_asiento(self,nro_asiento:int):
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
    def obtener_fecha(self):
        return self.fecha_hora

class GestorReservas:
    def __init__(self, unidad: Unidad, reservas: list[Reserva]):
        self.unidad = unidad
        self.reservas = reservas
    #asignacion
    def asignar_unidad(self, unidad: Unidad):
        self.unidad = unidad
    #insercion
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
            nro_asiento = reserva.obtener_asiento_numero()
            self.unidad.cambiar_estado_asiento(nro_asiento)
        self.reservas.clear()
    #Consultas
    def obtener_asientos_libres(self) -> list[Asiento]:
        return self.unidad.obtener_asientos_libres()
    def esta_reservado(self, nro_asiento: int) -> bool:
        for reserva in self.reservas:
            if reserva.obtener_asiento_numero() == nro_asiento:
                return True
        return False



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
        return f"{self.nombre_metodo} - Nombre Titular {self.nombre_pasajero} - DNI {self.dni_titular} - Número Tarjeta {self.numero} - Vencimiento {self.fecha_vencimiento.strftime('%d/%m/%Y')}"
   
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
    
class Venta: 
    def __init__(self, _fecha_Hora: datetime, a_asiento: Asiento, p_pasajero: Pasajero, m_pago: MedioPago):
        self.fecha_hora = _fecha_Hora
        self.asiento = a_asiento
        self.pasajero= p_pasajero
        self.medio_pago= m_pago
        self.concretada= False
    def verificar_pago_valido(self):            #Se fija si el medio de pago es válido
        return self.medio_pago.validarPago()
    def concretar_venta(self):
        if self.verificar_pago_valido(): self.concretada= True
    def obtener_nro_asiento(self):
        return self.asiento.obtener_numero()
    def obtener_registro_venta(self):
        print(f"Registro de Venta - {self.fecha_hora.day}/{self.fecha_hora.month}/{self.fecha_hora.year} {self.fecha_hora.strftime('%H:%M:%S')}")
        print(f"- Datos Pasajero: {self.pasajero.obtener_nombre()} - DNI {self.pasajero.obtener_dni()}")
        print(f"- Asiento Reservado: {self.asiento.obtener_numero()}")
        print(f"- Medio de Pago: {self.medio_pago.obtener_datos_pago()}")

class VerificadorReserva:
    def __init__(self, reservas: list[Reserva], unidad: Unidad):
        self.reservas = reservas
        self.unidad = unidad
    
   


class Servicio:
    def __init__(self, unidad: Unidad, calidad: str, precio: float, itinerario: Itinerario):
        self.unidad = unidad
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario
        self.ventas: list[Venta] = []
        self.reservas: list[Reserva] = []
        self.gestor_reservas = GestorReservas(self.unidad, self.reservas)
#Asignaciones
    def asignar_unidad(self, unidad:Unidad):
        self.unidad= unidad
        self.gestor_reservas.asignar_unidad(unidad)
    def asignar_itinerario(self, itinerario: Itinerario):
        self.itinerario = itinerario
#Inserciones
    def agregar_reserva(self, reserva: Reserva) -> bool:
        return self.gestor_reservas.agregar_reserva(reserva)
#Consultas
    def obtener_asientos_libres(self):
        return self.unidad.obtener_asientos_libres()
#liberacion de reservas (se llama 30 min antes del viaje):
    def liberar_asientos_reservados(self):
       self.gestor_reservas.liberar_asientos_reservados()
    
################################################ CLASE SISTEMA ################################

class ArgentinaTur:
    def __init__(self):
        self.sistema_activo = True
