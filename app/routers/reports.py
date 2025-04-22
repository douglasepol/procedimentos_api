from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app import crud, schemas
from app.database import SessionLocal
from app.dependencies import verificar_chave

router = APIRouter(
    prefix="/relatorios",
    tags=["relatorios"],
    dependencies=[Depends(verificar_chave)]
)

def obter_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/diario", response_model=list[schemas.ItemRelatorioDiario])
def diario(dia: date = Query(...), db: Session = Depends(obter_db)):
    return crud.relatorio_diario(db, dia)

@router.get("/glosas", response_model=schemas.ItemRelatorioGlosas)
def glosas(
    inicio: date = Query(...),
    fim: date = Query(...),
    db: Session = Depends(obter_db)
):
    item = crud.relatorio_glosas(db, inicio, fim)
    return {"quantidade": item.quantidade or 0, "total_valor": item.total_valor or 0.0}

@router.get("/financeiro", response_model=schemas.ItemRelatorioFinanceiro)
def financeiro(medico_id: int = Query(...), db: Session = Depends(obter_db)):
    item = crud.relatorio_financeiro(db, medico_id)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Nenhum dado para esse médico")
    return {"medico_id": item.medico_id, "total_valor": item.total_valor}
