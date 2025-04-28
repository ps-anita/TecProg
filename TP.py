from abc import ABC, abstractmethod
from typing import Tuple
from datetime import datetime, date
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
    def verificar_asiento_libre(self, nro_asiento:int)->bool:
        return self.asientos[nro_asiento -1].verificar_libre()
    def cambiar_estado_asiento(self,nro_asiento:int):
        self.asientos[nro_asiento - 1].cambiar_estado()
    def obtener_patente(self): return self.patente
    def obtener_asientos_libres(self):
        for i in self.asientos:
            if(i.verificar_libre()): 
                print(i.obtener_numero(),end=" ")

class Ciudad:
    def __init__(self, codigo: str, nombre: str, provincia: str):
        self.codigo = codigo 
        self.nombre = nombre 
        self.provincia = provincia
    def obtener_codigo(self): return self.codigo
    def obtener_nombre(self): return self.nombre
    def obtener_provincia(self): return self.provincia

class Itinerario:
    def __init__(self):
        self.paradas = []
    def agregar_parada(self, ciudad: Ciudad, fecha_hora: datetime):
        nueva_parada = {"ciudad": ciudad,"fecha_hora": fecha_hora}
        index = self.__obtener_posicion(fecha_hora)
        self.paradas.insert(index, nueva_parada)
    def obtener_partida(self):
        return self.paradas[0]
    def obtener_llegada(self):
        return self.paradas[-1]
    def mostrar_paradas(self):
        for parada in self.paradas:
            print("Ciudad: ", parada["ciudad"].obtener_nombre(), end =" --- ")
            print("Fecha: ", parada["fecha_hora"])
    def __obtener_posicion(self, fecha_hora):
        i = 0
        for parada in self.paradas:
            if fecha_hora > parada["fecha_hora"]:
                i = i + 1
            else:
                break
        return i

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
    def obtener_asiento_numero(self): return self.asiento.obtener_numero()
    def obtener_fecha(self):return self.fecha_hora
    def obtener_dni_pasajero(self): return self.pasajero.obtener_dni()

class GestorReservas:
    def __init__(self, reservas: list[Reserva], unidad: Unidad):
        self.unidad = unidad
        self.reservas = reservas
    #insercion | eliminación
    def agregar_reserva(self, reserva: Reserva) -> bool:
        nro_asiento = reserva.obtener_asiento_numero()
        if not self.unidad.verificar_asiento_libre(nro_asiento):
            print("El asiento seleccionado ya está ocupado.")
            return False
        self.reservas.append(reserva)
        self.unidad.cambiar_estado_asiento(nro_asiento)
        return True
    # liberar reserva en específico ya que se concretó la venta
    def liberar_reserva(self, nro_asiento: int):
        for reserva in self.reservas:
            if reserva.obtener_asiento_numero() == nro_asiento:
                self.unidad.cambiar_estado_asiento(nro_asiento)
                self.reservas.remove(reserva)
                break      
    #  se llama 30 min antes del viaje (las reservas que quedan no están con la venta concretada)
    def liberar_asientos_reservados(self):
        for reserva in self.reservas:                           #Va asiento por asiento cambiandole el estado a "Libre"
            nro_asiento = reserva.obtener_asiento_numero()
            self.unidad.cambiar_estado_asiento(nro_asiento)
        self.reservas.clear()
    #Consultas
    def verificar_pasajero_correcto(self, nro_asiento: int, pasajero: Pasajero) -> bool:
        #Verifica si el asiento reservado pertenece al pasajero
        for reserva in self.reservas:
            if reserva.obtener_asiento_numero() == nro_asiento and reserva.obtener_dni_pasajero() == pasajero.obtener_dni():
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

class ServicioExternoPago:
    def __init__(self, m_pago:MedioPago):
        self.medio_pago=m_pago
    def verificar_pago(self)->bool:
        return random.choice([True,False,True])

class TarjetaCredito(MedioPago):
    def __init__(self, numero: str, dni_t: int, nombre_pasajero: str, f_vencimiento: date, servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Tarjeta de Crédito"
        self.numero = numero
        self.dni_titular = dni_t
        self.nombre_pasajero = nombre_pasajero
        self.fecha_vencimiento = f_vencimiento
        self.servicio_externo= servicio_externo
    def validarPago(self): return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self): return f"{self.nombre_metodo} - Nombre Titular {self.nombre_pasajero} - DNI {self.dni_titular} - Número Tarjeta {self.numero} - Vencimiento {self.fecha_vencimiento.strftime('%d/%m/%Y')}"
   
class MercadoPago(MedioPago):
    def __init__(self, celular: str, email: str, servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Mercado Pago"
        self.celular = celular
        self.email = email
        self.servicio_externo= servicio_externo
    def validarPago(self):
        return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self):
        return f"{self.nombre_metodo} - Celular {self.celular} - Email {self.email}"

class Uala(MedioPago):
    def __init__(self, email: str, nombre_t: str,servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Ualá"
        self.email = email
        self.nombre_titular = nombre_t
        self.servicio_externo= servicio_externo
    def validarPago(self):
        return self.servicio_externo.verificar_pago()
    def obtener_datos_pago(self):
        return f"{self.nombre_metodo} - Nombre Titular {self.nombre_titular} - Email {self.email}"
    
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
        self.concretada= True
    def obtener_nro_asiento(self):
        return self.asiento.obtener_numero()
    def obtener_pasajero(self):
        return self.pasajero.obtener_nombre() + " " + self.pasajero.obtener_apellido()
    def obtener_registro_venta(self):
        print(f"Registro de Venta - {self.fecha_hora.day}/{self.fecha_hora.month}/{self.fecha_hora.year} {self.fecha_hora.strftime('%H:%M:%S')}")
        print(f"- Datos Pasajero: {self.pasajero.obtener_nombre()} - DNI {self.pasajero.obtener_dni()}")
        print(f"- Asiento Reservado: {self.asiento.obtener_numero()}")
        print(f"- Medio de Pago: {self.medio_pago.obtener_datos_pago()}")

    def obtener_fecha_hora(self):
        return self.fecha_hora
    
    def obtener_medio_pago(self):
        return self.medio_pago.__class__.__name__

class GestorVentas:
    def __init__(self, ventas: list[Venta], gestor_reservas: GestorReservas, unidad: Unidad):
        self.ventas = ventas
        self.gestor_reservas = gestor_reservas  # Recibe GestorReservas
        self.unidad = unidad
    def agregar_venta(self, venta: Venta) -> bool:
        nro_asiento = venta.obtener_nro_asiento()
        # Verificar si el asiento está reservado
        if self.unidad.verificar_asiento_libre(nro_asiento):
            # Si ya está reservado, verificar si es el mismo pasajero
            if self.gestor_reservas.verificar_pasajero_correcto(nro_asiento, venta.pasajero):
                return self.proceder_con_venta(venta)
            else:
                print(f"Asiento {nro_asiento} ya está reservado por otro pasajero.")
                return False
        else:
            # Si no está reservado, venderlo y marcar como ocupado
            self.unidad.cambiar_estado_asiento(nro_asiento)  # Cambiar el estado del asiento a ocupado
            return self.proceder_con_venta(venta)

    def proceder_con_venta(self, venta: Venta) -> bool:
        #Procede con la venta: verifica el pago
        if venta.verificar_pago_valido():
            venta.concretar_venta()
            self.ventas.append(venta)
            nro_asiento = venta.obtener_nro_asiento()
            print(f"Asiento {nro_asiento} vendido a {venta.obtener_pasajero()}.")
            self.gestor_reservas.liberar_reserva(nro_asiento)
            return True
        else:
            print(f"Pago inválido para el pasajero {venta.obtener_pasajero()}. No se logró realizar la venta.")
            return False

class Servicio:
    def __init__(self, unidad: Unidad, calidad: str, precio: float, itinerario: Itinerario,fecha_hora_salida: datetime, reservas: list[Reserva], ventas: list[Venta],  gestor_reservas: GestorReservas, gestor_ventas: GestorVentas):
        self.unidad = unidad
        self.calidad = calidad
        self.precio = precio
        self.itinerario = itinerario
        self.ventas = ventas
        self.reservas = reservas
        self.gestor_reservas = gestor_reservas
        self.gestor_ventas = gestor_ventas
        self.fecha_hora_salida= fecha_hora_salida
    def modificar_precio(self,precio_nuevo):
        self.precio=precio_nuevo
    def modificar_itinerario(self,it:Itinerario):
        self.itinerario=it
#Inserciones
    def agregar_reserva(self, reserva: Reserva) -> bool:
        return self.gestor_reservas.agregar_reserva(reserva)
    def agregar_venta(self,venta:Venta)->bool:
        return self.gestor_ventas.agregar_venta(venta)
#Consultas
    def obtener_asientos_libres(self):
        return self.unidad.obtener_asientos_libres()
    def obtener_calidad(self): return self.calidad
    def obtener_precio(self): return self.precio
    def obtener_itinerario(self): return self.itinerario.mostrar_paradas()
    def obtener_unidad(self): return self.unidad
    def obtener_fecha_salida(self): return self.fecha_hora_salida
#liberacion de reservas (se llama 30 min antes del viaje):
    def liberar_asientos_reservados(self):
       self.gestor_reservas.liberar_asientos_reservados()

    def obtener_ventas_por_tiempo(self, desde: datetime, hasta: datetime):
        cant = 0
        for venta in self.ventas:
            if venta.obtener_fecha_hora() <= desde and venta.fecha_hora >= hasta:
                cant = cant + 1
        return (self.precio * cant)

    def obtener_ventas_por_medio(self, medio):
        cant = 0
        for venta in self.ventas: 
            if venta.obtener_medio_pago() == medio:
                cant = cant + 1
        return (self.precio * cant)

#-----------------------------------------------------Factory-------------------------------------------------#
class ServicioFactory:
    @staticmethod
    def crear_servicio(unidad: Unidad, calidad: str, precio: float,
                        itinerario: Itinerario, fecha_hora_salida: datetime) -> Servicio:
        reservas:list[Reserva] = []
        ventas:list[Venta] = []
        
        gestor_reservas = GestorReservas(reservas, unidad)
        gestor_ventas = GestorVentas(ventas, gestor_reservas, unidad)
        
        servicio = Servicio(unidad, calidad, precio, itinerario, fecha_hora_salida,
                             reservas, ventas, gestor_reservas, gestor_ventas)
        
        return servicio
    
################################################ CLASE SISTEMA ################################################
class ArgenTur:
    def __init__(self):
        self.sistema_activo = True
        self.lista_servicios: list[Servicio] = []
        self.lista_ciudades: list[Ciudad] = []
        self.lista_itinerarios: list[Itinerario] = []
        self.lista_unidades: list[Unidad]
        self.servicio_factory = ServicioFactory()

    #### MÉTODOS AGREGAR Y CREAR ####
    # Recibe una lista de tuplas de cada ciudad con su fecha y hora de salida
    def crear_itinerario(self,paradas:list[Tuple[Ciudad,datetime]]):
        it= Itinerario()
        for ciudad, fecha in paradas:
            it.agregar_parada(ciudad,fecha)
        self.lista_itinerarios.append(it)

    def crear_servicio(self, unidad: Unidad, calidad:str, precio:float, itinerario: Itinerario,fecha_hora: datetime):
        servicio = self.servicio_factory.crear_servicio(unidad, calidad, precio, itinerario, fecha_hora)
        self.lista_servicios.append(servicio)

    def reservar_pasajes(self, pasajero:Pasajero, fecha_hora_reserva: datetime, asiento: Asiento, servicio: Servicio):
        reserva=Reserva(fecha_hora_reserva,asiento,pasajero)
        if(servicio.agregar_reserva(reserva)):
            print("Reserva realizada con éxito.")

    def agregar_ciudad(self, cod: str, nombre: str, prov: str):
        self.lista_ciudades.append(Ciudad(cod,nombre,prov))
        
    def agregar_unidad(self,patente: str):
        self.lista_unidades.append(Unidad(patente))
    
    def realizar_compra(self, fecha_hora: datetime, asiento: Asiento, pasajero:Pasajero, servicio_solicitado: Servicio, m_pago:MedioPago):
        servicio_solicitado.agregar_venta(Venta(fecha_hora,asiento,pasajero,m_pago))
    
    #### MÉTODOS CONSULTAS ####
    def obtener_itinerario(self,nro:int)-> Itinerario:   # Esto lo pensé así: Cada itineraro está enumerado (línea x), el encargado de crear servicios va a ver
        return self.lista_itinerarios[nro-1]             # la lista de it, elegir el # de it y al colocar ese número en este método, le devuelve toda la info del it que quiere
        
    def obtener_servicio(self, nro:int)-> Servicio:
        return self.lista_servicios[nro-1]

    def ver_ciudades(self):
        for i in self.lista_ciudades:
            print(f"{i.obtener_codigo} - {i.obtener_nombre}, {i.obtener_provincia}")
        
    def ver_unidades(self):
        for unidad in self.lista_unidades:
            print(f"Unidad patente {unidad.obtener_patente()}")

    def ver_lista_itinerarios(self):
        cont=1 #Es solo por estética
        for it in self.lista_itinerarios:
            print("Itinerario #",cont)
            it.mostrar_paradas()
            print()
            cont+=1

    def ver_asientos_libres(self, s: Servicio):
        unidad=s.obtener_unidad()
        print(f"Asientos libres de Unidad {unidad.obtener_patente()}")
        s.obtener_asientos_libres()
    
    def ver_servicios(self):
        cont=1 #También es por estetica
        for servicio in self.lista_servicios:
            uni=servicio.obtener_unidad()
            print(f"SERVICIO #{cont}")
            print(f"Fecha y Hora de salida: {servicio.obtener_fecha_salida()}")
            print(f"Calidad: {servicio.obtener_calidad()} - Unidad: {uni.obtener_patente()} - Precio ${servicio.obtener_precio()}")
            print("Itinerario del Servicio:")
            servicio.obtener_itinerario()
            print("Asientos Libres:")
            uni.obtener_asientos_libres()
            print()
            cont+=1

    def ver_total_por_fecha(self, desde: datetime, hasta: datetime):
        total = 0
        for servicio in self.lista_servicios:
            total = total + servicio.obtener_ventas_por_tiempo(desde, hasta)
        return total

    def ver_total_por_medio(self, medio: str):
        total = 0
        for servicio in self.lista_servicios:
            total = total + servicio.obtener_ventas_por_medio(medio)
        return total
    
################################################ MAIN ################################################

arg=ArgenTur()
c1=Ciudad(1,"a","a")
c2=Ciudad(2,"b","b")
c3=Ciudad(3,"c","c")
c4=Ciudad(4,"d","d")
c5=Ciudad(5,"e","e")

a1=Asiento(1)
a2=Asiento(22)
a3=Asiento(3)

p1=Pasajero("Viviana","Santucci","vivi@fich.unl",12345678)
p2=Pasajero("Pablo","Novara","cucarachasracing@fich.unl",87654321)

tu=[(c1,datetime(2025,4,27,13,00)),(c2,datetime(2025,4,28,14,00)),(c3,datetime(2025,4,29,15,00))]
tu2=[(c4,datetime(2026,3,15,10,00)),(c5,datetime(2026,3,15,16,00))]

arg.crear_itinerario(tu)
arg.crear_itinerario(tu2)

arg.crear_servicio(Unidad("A5"),"estandar",100,arg.obtener_itinerario(1),datetime(2025,4,28,14,00))
arg.crear_servicio(Unidad("A3"),"estandar",100,arg.obtener_itinerario(2),datetime(2026,4,28,14,00))
arg.ver_servicios()
s1=arg.obtener_servicio(1)
s2=arg.obtener_servicio(2)

print()
print("RESERVA VIVIANA")
arg.reservar_pasajes(p1,datetime(15,2,9,15,23),a1,s1)
print()
print("RESERVA PABLO")
arg.reservar_pasajes(p2,datetime(15,2,9,15,23),a1,s1)

print("RESERVA PABLO INTENTO 2")
arg.reservar_pasajes(p2,datetime(15,2,9,15,23),a2,s1)

print()
print("ASIENTOS DISPONIBLES")
arg.ver_asientos_libres(s1)