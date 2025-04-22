from datetime import date
from pydantic import BaseModel
from typing import Optional
from app.models import StatusPagamento

class ProcedimentoBase(BaseModel):
    medico_id: int
    paciente_id: int
    data_procedimento: date
    valor_procedimento: float
    status_pagamento: StatusPagamento

class ProcedimentoCriar(ProcedimentoBase):
    pass

class Procedimento(ProcedimentoBase):
    id: int

    class Config:
        orm_mode = True

# Itens de relatório

class ItemRelatorioDiario(BaseModel):
    medico_id: int
    total_procedimentos: int

class ItemRelatorioGlosas(BaseModel):
    quantidade: int
    total_valor: float

class ItemRelatorioFinanceiro(BaseModel):
    medico_id: int
    total_valor: float
