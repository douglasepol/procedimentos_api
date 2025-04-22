from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

CHAVE_API = "123456"
NOME_HEADER = "X-API-Key"
api_key_header = APIKeyHeader(name=NOME_HEADER, auto_error=False)

def verificar_chave(api_key: str = Security(api_key_header)):
    if api_key != CHAVE_API:
        raise HTTPException(status_code=403, detail="Chave de API inválida")
    return api_key
