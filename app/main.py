from fastapi import FastAPI
from app.routers import procedures, reports

app = FastAPI(title="API de Procedimentos Médicos")

app.include_router(procedures.router)
app.include_router(reports.router)
