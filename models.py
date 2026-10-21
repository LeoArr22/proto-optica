from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(150), nullable=False, index=True)
    dni = Column(String(20), nullable=True, index=True)
    telefono = Column(String(50), nullable=True)
    observaciones = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    # Relación renombrada a fichas
    fichas = relationship("HistorialOptico", back_populates="cliente", order_by="desc(HistorialOptico.fecha)")


class HistorialOptico(Base):
    __tablename__ = "historiales_opticos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    tipo_atencion = Column(String(100), default="Control / Graduación")
    medidas_tomadas = Column(String(20), default="Sí")
    compro = Column(String(20), default="Sí")

    # Ojo Derecho (OD)
    od_esfera = Column(String(20), default="0.00")
    od_cilindro = Column(String(20), default="0.00")
    od_eje = Column(String(20), default="0°")
    od_adicion = Column(String(20), default="")

    # Ojo Izquierdo (OI)
    oi_esfera = Column(String(20), default="0.00")
    oi_cilindro = Column(String(20), default="0.00")
    oi_eje = Column(String(20), default="0°")
    oi_adicion = Column(String(20), default="")

    distancia_interpupilar = Column(String(20), default="")
    armazon = Column(String(100), default="")
    cristales = Column(String(100), default="")
    notas_trabajo = Column(Text, nullable=True)

    cliente = relationship("Cliente", back_populates="fichas")