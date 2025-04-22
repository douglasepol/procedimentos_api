from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import SessionLocal, engine, Base
from app.dependencies import verificar_chave

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/procedimentos",
    tags=["procedimentos"],
    dependencies=[Depends(verificar_chave)]
)

def obter_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Procedimento)
def criar(proc: schemas.ProcedimentoCriar, db: Session = Depends(obter_db)):
    return crud.criar_procedimento(db, proc)

@router.get("/", response_model=list[schemas.Procedimento])
def listar(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1), db: Session = Depends(obter_db)):
    return crud.listar_procedimentos(db, skip, limit)

@router.get("/{proc_id}", response_model=schemas.Procedimento)
def detalhar(proc_id: int, db: Session = Depends(obter_db)):
    proc = crud.obter_procedimento(db, proc_id)
    if not proc:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    return proc

@router.patch("/{proc_id}", response_model=schemas.Procedimento)
def atualizar(proc_id: int, status: models.StatusPagamento = Query(...), db: Session = Depends(obter_db)):
    resultado = crud.atualizar_status(db, proc_id, status)
    if not resultado:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    return resultado
