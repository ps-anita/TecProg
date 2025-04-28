from abc import ABC, abstractmethod
from typing import Tuple
from datetime import datetime, time
import random
import threading

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
        self.asientos: list[Asiento] = [Asiento(i) for i in range(1, 21)] # genera lista con 20 asientos desocupados (list comprehension)
    def verificar_asiento_libre(self, nro_asiento:int)->bool:
        return self.asientos[nro_asiento - 1].verificar_libre()
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
    def __init__(self, fecha_hora: datetime, asiento: Asiento, pasajero:Pasajero,unidad:Unidad):
        self.fecha_hora = fecha_hora
        self.asiento = asiento
        self.pasajero = pasajero
        self.unidad=unidad
    #consultas
    def obtener_asiento_numero(self): return self.asiento.obtener_numero()
    def obtener_fecha(self):return self.fecha_hora
    def obtener_dni_pasajero(self): return self.pasajero.obtener_dni()
    def obtener_unidad(self): return self.unidad

class GestorReservas:
    def __init__(self, reservas: list[Reserva]):
        self.reservas = reservas
    #insercion | eliminación
    def agregar_reserva(self, reserva: Reserva)->bool:
        nro_asiento = reserva.obtener_asiento_numero()
        unidad=reserva.obtener_unidad()
        unidad.cambiar_estado_asiento(nro_asiento)
        self.reservas.append(reserva)
    # liberar reserva en específico ya que se concretó la venta
    def liberar_reserva(self, nro_asiento: int):
        for reserva in self.reservas:
            if reserva.obtener_asiento_numero() == nro_asiento:
                unidad=reserva.obtener_unidad()
                unidad.cambiar_estado_asiento(nro_asiento)
                self.reservas.remove(reserva)
                break      
    #  se llama 30 min antes del viaje (las reservas que quedan no están con la venta concretada)
    def liberar_asientos_reservados(self):
        for reserva in self.reservas:                           #Va asiento por asiento cambiandole el estado a "Libre"
            nro_asiento = reserva.obtener_asiento_numero()
            unidad=reserva.obtener_unidad()
            unidad.cambiar_estado_asiento(nro_asiento)
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
    @abstractmethod
    def obtener_nombre(self):
        pass

class ServicioExternoPago:
    def verificar_pago(self)->bool:
        return random.choice([True,False,True])

class TarjetaCredito(MedioPago):
    def __init__(self, numero: str, dni_t: int, nombre_pasajero: str, f_vencimiento: datetime, servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Tarjeta de Crédito"
        self.numero = numero
        self.dni_titular = dni_t
        self.nombre_pasajero = nombre_pasajero
        self.fecha_vencimiento = f_vencimiento
        self.servicio_externo= servicio_externo
    def validarPago(self): return self.servicio_externo.verificar_pago()
    def obtener_nombre(self): return self.nombre_metodo
    def obtener_datos_pago(self): return f"{self.nombre_metodo} - Nombre Titular {self.nombre_pasajero} - DNI {self.dni_titular} - Número Tarjeta {self.numero} - Vencimiento {self.fecha_vencimiento.strftime('%d/%m/%Y')}"
   
class MercadoPago(MedioPago):
    def __init__(self, celular: str, email: str, servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Mercado Pago"
        self.celular = celular
        self.email = email
        self.servicio_externo= servicio_externo
    def validarPago(self): return self.servicio_externo.verificar_pago()
    def obtener_nombre(self): return self.nombre_metodo
    def obtener_datos_pago(self): return f"{self.nombre_metodo} - Celular {self.celular} - Email {self.email}"

class Uala(MedioPago):
    def __init__(self, email: str, nombre_t: str,servicio_externo:ServicioExternoPago):
        self.nombre_metodo="Ualá"
        self.email = email
        self.nombre_titular = nombre_t
        self.servicio_externo= servicio_externo
    def validarPago(self): return self.servicio_externo.verificar_pago()
    def obtener_nombre(self): return self.nombre_metodo
    def obtener_datos_pago(self): return f"{self.nombre_metodo} - Nombre Titular {self.nombre_titular} - Email {self.email}"
    
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
        return self.medio_pago

class GestorVentas:
    def __init__(self, ventas: list[Venta], gestor_reservas: GestorReservas, unidad: Unidad):
        self.ventas = ventas
        self.gestor_reservas = gestor_reservas  # Recibe GestorReservas
        self.unidad = unidad
    def proceder_con_venta(self, venta: Venta) -> bool:
        #Procede con la venta: verifica el pago
        if venta.verificar_pago_valido():
            venta.concretar_venta()
            self.ventas.append(venta)
            nro_asiento = venta.obtener_nro_asiento()
            print(f"Asiento {nro_asiento} vendido a {venta.obtener_pasajero()}.")
            return True
        else:
            print(f"Pago inválido para el pasajero {venta.obtener_pasajero()}. No se logró realizar la venta.")
            return False
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
            return self.proceder_con_venta(venta)
    def obtener_monto_ventas_por_tiempo(self, desde: datetime, hasta: datetime, precio:float):
        cant = 0
        for venta in self.ventas:
            if desde <= venta.obtener_fecha_hora() <= hasta:
                cant += 1
        return (precio * cant)
    def obtener_ventas_por_medio(self, medio:str, desde:datetime, hasta:datetime, precio:float):
        cant = 0
        for venta in self.ventas: 
            m_pago=venta.obtener_medio_pago()
            if m_pago.obtener_nombre() == medio and desde <= venta.obtener_fecha_hora() <= hasta:
                cant += 1
        return precio * cant
    def obtener_cantidad_ventas_por_medio(self, medio:str, desde:datetime, hasta:datetime):
        cant = 0
        for venta in self.ventas: 
            m_pago=venta.obtener_medio_pago()
            if m_pago.obtener_nombre() == medio and desde <= venta.obtener_fecha_hora() <= hasta:
                cant += 1
        return cant

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
        self.iniciar_liberacion_asientos()
    def modificar_precio(self,precio_nuevo):
        self.precio=precio_nuevo
    def modificar_itinerario(self,it:Itinerario):
        self.itinerario=it
#Inserciones
    def _agregar_reserva(self, reserva: Reserva):
        return self.gestor_reservas.agregar_reserva(reserva)
    def agregar_venta(self,venta:Venta)->bool:
        return self.gestor_ventas.agregar_venta(venta)
#Consultas
    def obtener_asientos_libres(self):
        return self.unidad.obtener_asientos_libres()
    def obtener_calidad(self): return self.calidad
    def obtener_precio(self): return self.precio
    def obtener_itinerario(self): return self.itinerario.mostrar_paradas()
    def obtener_llegada(self): return self.itinerario.obtener_llegada()
    def obtener_unidad(self): return self.unidad
    def obtener_fecha_salida_str(self):
        return f"{self.fecha_hora_salida.day}/{self.fecha_hora_salida.month}/{self.fecha_hora_salida.year}"
    def obtener_fecha_salida_datetime(self): return self.fecha_hora_salida
    def consultar_asiento_disponible(self,nro_asiento:int):
        return self.unidad.verificar_asiento_libre(nro_asiento)
    def obtener_monto_ventas(self, desde: datetime, hasta: datetime): return self.gestor_ventas.obtener_monto_ventas_por_tiempo(desde,hasta,self.obtener_precio())
    def discriminar_ventas_por_pagos(self,medio:str,desde:datetime, hasta:datetime): return self.gestor_ventas.obtener_ventas_por_medio(medio,desde,hasta,self.precio)
    def obtener_cantidad_ventas_por_medio(self, medio:str,desde:datetime,hasta:datetime):return self.gestor_ventas.obtener_cantidad_ventas_por_medio(medio,desde,hasta)
    def iniciar_liberacion_asientos(self):
         # Inicia un hilo que liberará los asientos 30 minutos antes de la salida del viaje.
         tiempo_restante = (self.fecha_hora_salida - datetime.now()).total_seconds()
         # Tiempo para liberar los asientos (30 minutos antes)
         tiempo_para_liberar = tiempo_restante - 1800  # 1800 segundos = 30 minutos
         # Validar si el tiempo para liberar es mayor a 1 día (86400 segundos)
         if tiempo_para_liberar <= 0:
             print("El viaje ya ha pasado o está a menos de 30 minutos de la salida, liberando asientos ahora...")
             self.liberar_asientos_reservados()
         elif tiempo_para_liberar > 60 * 60 * 24:  # mayor a 1 día (86400 segundos)
             print("El tiempo de espera es mayor a 1 día, liberación cancelada.")
         else:
             # Crear y comenzar el hilo que liberará los asientos
             threading.Timer(tiempo_para_liberar, self.liberar_asientos_reservados).start()

    #liberacion de reservas (se llama 30 min antes del viaje):
    def liberar_asientos_reservados(self):
       self.gestor_reservas.liberar_asientos_reservados()
#-----------------------------------------------------Factory-------------------------------------------------#
class ServicioFactory:
    @staticmethod
    def crear_servicio(unidad: Unidad, calidad: str, precio: float, itinerario: Itinerario, fecha_hora_salida: datetime) -> Servicio:
        reservas:list[Reserva] = []
        ventas:list[Venta] = []
        
        gestor_reservas = GestorReservas(reservas)
        gestor_ventas = GestorVentas(ventas, gestor_reservas, unidad)
        
        servicio = Servicio(unidad, calidad, precio, itinerario, fecha_hora_salida, reservas, ventas, gestor_reservas, gestor_ventas)
        
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
        reserva=Reserva(fecha_hora_reserva,asiento,pasajero,servicio.obtener_unidad())
        servicio._agregar_reserva(reserva)
        print(f"Reserva realizada! Pasajero {pasajero.nombre} {pasajero.apellido}, asiento {asiento.obtener_numero()}, servicio del {servicio.obtener_fecha_salida_str()}")

    def agregar_ciudad(self, cod: str, nombre: str, prov: str):
        self.lista_ciudades.append(Ciudad(cod,nombre,prov))
        
    def agregar_unidad(self,patente: str):
        self.lista_unidades.append(Unidad(patente))
    
    def realizar_compra(self, fecha_hora: datetime, asiento: Asiento, pasajero:Pasajero, servicio_solicitado: Servicio, m_pago:MedioPago):
        return servicio_solicitado.agregar_venta(Venta(fecha_hora,asiento,pasajero,m_pago))
    
    def verificar_asiento(nro_asiento:int, servicio: Servicio)->bool:
        return servicio.consultar_asiento_disponible(nro_asiento)
    
    def liberar_asientos_caducados(self):
        hora_actual=datetime(2025,3,29,17,48)
        for servicio in self.lista_servicios:
            
            servicio.iniciar_liberacion_asientos()
            
    
    #### MÉTODOS CONSULTAS ####
    def obtener_itinerario(self,nro:int)-> Itinerario:   # Esto lo pensé así: Cada itineraro está enumerado (línea 340), el encargado de crear servicios va a ver
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
        print(f"Asientos libres de la unidad {unidad.obtener_patente()}")
        s.obtener_asientos_libres()
        print()
    
    def ver_servicios(self):
        cont=1 #También es por estetica
        for servicio in self.lista_servicios:
            uni=servicio.obtener_unidad()
            print(f"SERVICIO #{cont}")
            print(f"Fecha y Hora de salida: {servicio.obtener_fecha_salida_str()}")
            print(f"Calidad: {servicio.obtener_calidad()} - Unidad: {uni.obtener_patente()} - Precio ${servicio.obtener_precio()}")
            print("Itinerario del Servicio:")
            servicio.obtener_itinerario()
            print()
            cont+=1
    def ver_monto_total_por_fecha(self, desde: datetime, hasta: datetime)->int:
        total = 0
        for servicio in self.lista_servicios:
            total += servicio.obtener_monto_ventas(desde, hasta)
        return total
    def ver_total_por_medio_pago(self, medio: str,desde: datetime,hasta: datetime)->int:
        total = 0
        for servicio in self.lista_servicios:
            total = total + servicio.discriminar_ventas_por_pagos(medio,desde,hasta)
        return total
    def ver_cantidad_por_medio_pago(self, medio: str,desde: datetime,hasta: datetime)->int:
        cantidad = 0
        for servicio in self.lista_servicios:
            cantidad = cantidad + servicio.obtener_cantidad_ventas_por_medio(medio,desde,hasta)
        return cantidad

    def ver_cantidad_viajes_por_destino(self, desde: datetime, hasta: datetime):
        for itinerario in self.lista_itinerarios:
            destino = itinerario.obtener_llegada()
            print(f"  - Destino: {destino['ciudad'].obtener_nombre()},  {destino['ciudad'].obtener_provincia()} ")  # Para ver la estructura del diccionario destino
            cantidad_viajes = 0
            for servicio in self.lista_servicios:
                llegada_servicio = servicio.obtener_llegada()
                if llegada_servicio["ciudad"].obtener_nombre() == destino["ciudad"].obtener_nombre() and desde <= llegada_servicio["fecha_hora"] <= hasta:
                    cantidad_viajes = cantidad_viajes + 1
            print(f"     - Viajes: {cantidad_viajes}")
    
    def generar_informe(self,desde: datetime,hasta: datetime):
        print(f"INFORME ARGENTUR {desde.day}/{desde.month}/{desde.year} - {hasta.day}/{hasta.month}/{hasta.year}")
        print(f"- Monto de ventas totales facturados: ${self.ver_monto_total_por_fecha(desde,hasta)}")
        print(f"- Cantidad de pagos realizados por:")
        print(f"  - Mercado Pago: {self.ver_cantidad_por_medio_pago('Mercado Pago',desde,hasta)}")
        print(f"  - Ualá: {self.ver_cantidad_por_medio_pago('Ualá',desde,hasta)}")
        print(f"  - Tarjeta de Crédito: {self.ver_cantidad_por_medio_pago('Tarjeta de Crédito',desde,hasta)}")
        print(f"- Cantidad de viajes realizados por localidad: ")
        self.ver_cantidad_viajes_por_destino(desde,hasta)

    def verificar_asiento(self,nro_asiento:int ,servicio:Servicio)->bool:
        return servicio.consultar_asiento_disponible(nro_asiento)
    
def cargar_datos()-> ArgenTur:      # Esta clase únicamente se encarga de ya crear servicios, ciudades e itinerarios para usar el programa.
    arg=ArgenTur()
    
    c1=Ciudad("3101","Paraná","Entre Ríos")
    c2=Ciudad("3000","Santa Fe","Santa Fe")
    c3=Ciudad("C1000","CABA","Buenos Aires")
    c4=Ciudad("4400","Los Noques","Salta")
    c5=Ciudad("T4000","San Miguel de Túcuman","Túcuman")
    c6=Ciudad("V9410","Ushuaia","Tierra del Fuego")
    c7=Ciudad("R8400","Bariloche","Río Negro")

    it1=[(c1,datetime(2025,8,2,8,00)),(c2,datetime(2025,8,2,9,00)),(c3,datetime(2025,8,17,00))]
    it2=[(c3,datetime(2025,10,15,10,00)),(c2,datetime(2025,10,15,16,00)),(c5,datetime(2025,10,16,4,00)),(c4,datetime(2025,10,16,11,00))]
    it3=[(c6,datetime(2025,5,5,13,00)),(c7,datetime(2025,5,5,15,00))]

    arg.crear_itinerario(it1)
    arg.crear_itinerario(it2)
    arg.crear_itinerario(it3)

    arg.crear_servicio(Unidad("AAA 505"),"Premium",50000,arg.obtener_itinerario(1),datetime(2025,8,2,8,00))
    arg.crear_servicio(Unidad("AAB 000"),"Estándar",30500,arg.obtener_itinerario(2),datetime(2025,10,15,10,00))
    arg.crear_servicio(Unidad("AAB 153"),"Estándar",20000,arg.obtener_itinerario(3),datetime(2025,5,5,13,00))

    # Reservo algunos lugares
    p1=Pasajero("Viviana","Santucci","vivianasantucci@fich.unl",2531462)
    p2=Pasajero("Jimena","Bourlot","jime_Bourlot@fich.unl",30654892)
    p3=Pasajero("Federico","Castoldi","castoldi@fich.unl",4562137)
    p4=Pasajero("Jesús Exequiel","Benavídez","jesusbenavidez@fich.unl",3576412)

    arg.reservar_pasajes(p1,datetime(2025,6,12,15,35),Asiento(10),arg.obtener_servicio(1))
    arg.reservar_pasajes(p2,datetime(2025,6,15,23,26),Asiento(15),arg.obtener_servicio(2))
    arg.reservar_pasajes(p3,datetime(2025,3,29,17,58),Asiento(3),arg.obtener_servicio(3))
    arg.reservar_pasajes(p4,datetime(2024,12,25,11,20),Asiento(19),arg.obtener_servicio(2))

    servicio_externo=ServicioExternoPago()
    arg.realizar_compra(datetime(2025,6,12,15,35),Asiento(10),p1,arg.obtener_servicio(1),MercadoPago(3421596846,p1.obtener_email(),servicio_externo)) 
    arg.realizar_compra(datetime(2025,1,16,23,26),Asiento(15),p2,arg.obtener_servicio(2),TarjetaCredito(1234567891023564,p2.obtener_dni(),p2.obtener_nombre(),datetime(2037,10,8),servicio_externo))
    arg.realizar_compra(datetime(2025,12,25,23,26),Asiento(19),p4,arg.obtener_servicio(2),TarjetaCredito(1234567891023564,p4.obtener_dni(),p4.obtener_nombre(),datetime(2037,10,8),servicio_externo))

    return arg

################################################ SIMULACIÓN DE PROGRAMA ################################################
arg=cargar_datos()

print(f"¡Bienvenidos a ArgenTur! El lugar donde podrás cumplir el sueño de conocer los lugares más atractivos del país. \nA continuación podrás conocer todos los servicios que tenemos para vos. \n")
arg.ver_servicios()

servicio_elegido=int(input("¿Cuál servicio te gustaría disfrutar? Para seleccionarlo, ingresa el #número correspondiente del servicio: "))
servicio=arg.obtener_servicio(servicio_elegido)

print("¡Estupendo! A continuación, te mostramos los asientos disponibles para este servicio.")
arg.ver_asientos_libres(servicio)

nro_asiento=int(input("\nPor favor, ingresa el número del asiento que te gustaría reservar: "))
while(not arg.verificar_asiento(nro_asiento,servicio)):
    nro_asiento=int(input("¡Error! Este asiento ya ha sido seleccionado por otro pasajero. Seleccione un nuevo asiento, por favor: "))

asiento = Asiento(nro_asiento)
print("\n¡Estás a un paso de disfrutar de este maravilloso viaje! Primero, conozcamonos un poco.")

nombre=input("¿Cuál es tu nombre? ")
apellido=input("¿Y tu apellido? ")
dni=input("¿Cómo es tu DNI? ")
email=(input("¡Último paso! Necesitamos un email para enviarte los detalles del servicio: "))

pasajero=Pasajero(nombre,apellido,email,dni)
arg.reservar_pasajes(pasajero,datetime(2025,4,28,12,00),asiento,servicio)

arg.ver_asientos_libres(servicio)

eleccion1 = int(input("\n¿Desea abonar el viaje en este momento y concretar la venta? \n1) Sí. \n2) No\n"))
if eleccion1 == 1:

    serv_ext=ServicioExternoPago()
    metodo=int(input("ArgenTur acepta tres tipos de métodos de pago. Seleccione la de su preferencia.\n1) Mercado Pago. \n2) Uala. \n3) Tarjeta de Crédito \n"))
    if metodo == 1:
        cel=int(input("Ingrese su celular, por favor: "))
        medio_pago = MercadoPago(cel,pasajero.obtener_email(),serv_ext)
    elif metodo == 2:
        medio_pago = Uala(pasajero.obtener_email(),pasajero.obtener_nombre(),serv_ext)
    elif metodo == 3:
        nro_tarjeta=int(input("Ingrese el número de la tarjeta: "))
        vencimiento=str(input("Ingrese la fecha de vencimiento de la tarjeta (mm/aaaa): "))
        medio_pago = TarjetaCredito(nro_tarjeta,pasajero.obtener_dni(),pasajero.obtener_nombre(),vencimiento,serv_ext)
    else:
        print("Método de pago no válido.")
        medio_pago = None

    if medio_pago:
        arg.realizar_compra(datetime.now(), asiento, pasajero, servicio, medio_pago)
else:
    print("Recuerde que 30 minutos antes del viaje, perderá el asiento en caso de no abonar.")
print("¡Muchas gracias por elegir viajar con nosotros")


print("\nBienvenido a la sección de informes. Por favor, ingrese el período en el que se desea ver el informe.")

desde=datetime
hasta=datetime

desde_dia=int(input("Día desde: "))
desde_mes=int(input("Mes desde: "))
desde_año=int(input("Año desde: "))

hasta_dia=int(input("Día hasta: "))
hasta_mes=int(input("Mes hasta: "))
hasta_año=int(input("Año hasta: "))

print("\nGENERANDO INFORME...\n")
arg.generar_informe(datetime(desde_año,desde_mes,desde_dia),datetime(hasta_año,hasta_mes,hasta_dia))
