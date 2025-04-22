from sqlalchemy import Column, Integer, Date, Float, Enum
from app.database import Base
import enum

class StatusPagamento(enum.Enum):
    pago = "pago"
    pendente = "pendente"
    glosado = "glosado"

class Procedimento(Base):
    __tablename__ = "procedimentos"

    id = Column(Integer, primary_key=True, index=True)
    medico_id = Column(Integer, nullable=False, index=True)
    paciente_id = Column(Integer, nullable=False, index=True)
    data_procedimento = Column(Date, nullable=False)
    valor_procedimento = Column(Float, nullable=False)
    status_pagamento = Column(Enum(StatusPagamento), nullable=False)
