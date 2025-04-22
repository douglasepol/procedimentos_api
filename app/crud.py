from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date
import app.models as models
import app.schemas as esquemas

def criar_procedimento(db: Session, proc: esquemas.ProcedimentoCriar):
    novo = models.Procedimento(**proc.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_procedimentos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Procedimento).offset(skip).limit(limit).all()

def obter_procedimento(db: Session, proc_id: int):
    return db.query(models.Procedimento).filter(models.Procedimento.id == proc_id).first()

def atualizar_status(db: Session, proc_id: int, status: models.StatusPagamento):
    proc = db.query(models.Procedimento).filter(models.Procedimento.id == proc_id).first()
    if proc:
        proc.status_pagamento = status
        db.commit()
        db.refresh(proc)
    return proc

def relatorio_diario(db: Session, dia: date):
    return db.query(
        models.Procedimento.medico_id,
        func.count(models.Procedimento.id).label("total_procedimentos")
    ).filter(models.Procedimento.data_procedimento == dia)\
     .group_by(models.Procedimento.medico_id).all()

def relatorio_glosas(db: Session, inicio: date, fim: date):
    return db.query(
        func.count(models.Procedimento.id).label("quantidade"),
        func.sum(models.Procedimento.valor_procedimento).label("total_valor")
    ).filter(
        and_(
            models.Procedimento.status_pagamento == models.StatusPagamento.glosado,
            models.Procedimento.data_procedimento >= inicio,
            models.Procedimento.data_procedimento <= fim
        )
    ).one()

def relatorio_financeiro(db: Session, medico_id: int):
    return db.query(
        models.Procedimento.medico_id,
        func.sum(models.Procedimento.valor_procedimento).label("total_valor")
    ).filter(models.Procedimento.medico_id == medico_id)\
     .group_by(models.Procedimento.medico_id).one_or_none()
