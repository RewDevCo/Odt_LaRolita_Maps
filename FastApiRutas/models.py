from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime
from database import Base
from sqlalchemy.sql import func


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)  
    method = Column(String(10))
    path = Column(String(255))
    status_code = Column(Integer)
    client_ip = Column(String(45))
    process_time = Column(Float)
    created_at = Column(DateTime, default=func.now())  


class Rutas(Base):
    __tablename__ = "rutas"

    id_rutas = Column(Integer, primary_key=True, index=True)
    code = Column(String(45))
    origen = Column(String(80))
    destino = Column(String(80))
    lv = Column(String(80))
    festivos = Column(String(80))
    total_paradas = Column(Integer)
    tiempo_espera = Column(String(80))
    fecha_publicacion = Column(Date)
    fecha_actualizacion = Column(Date)
    activo = Column(Integer)


class RutasCenefas(Base):
    __tablename__ = "rutas_cenefas"

    id = Column(Integer, primary_key=True, index=True)
    id_rutas = Column(Integer, ForeignKey('rutas.id_rutas'))
    id_cenefas = Column(Integer, ForeignKey('cenefas.id_cenefas'))


class Cenefas(Base):
    __tablename__ = "cenefas"

    id_cenefas = Column(Integer, primary_key=True, index=True)
    orden = Column(String(80))
    cenefa = Column(String(80))
    tipo = Column(String(45))
    modulo = Column(String(45))
    cantidad_mm = Column(String(45))
    estado_del_multiple = Column(String(80))
    nombre = Column(String(80))
    direccion_bandera = Column(String(80))
    localidad = Column(String(80))
    consola = Column(String(80))
    panel = Column(String(80))
    audio = Column(String(80))
    longitud = Column(Float) 
    latitud = Column(Float)  
    zona = Column(String(45))
