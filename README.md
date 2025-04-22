# API de Procedimentos Médicos

API REST para cadastro de procedimentos médicos, relatórios de glosas e financeiros.

---

## Tecnologias

- **Python 3.9+**  
- **FastAPI**  
- **Uvicorn** (servidor ASGI)  
- **SQLite** + **SQLAlchemy**  
- **Pydantic**  
- **Swagger/OpenAPI** (documentação automática em `/docs`)

---

## Instalação e Configuração

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/seu-usuario/procedimentos_api.git
   cd procedimentos_api
   ```

2. **Crie e ative um ambiente virtual**  
   - **Linux/macOS**  
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```  
   - **Windows (PowerShell)**  
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```  

3. **Instale dependências**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Defina sua chave de API**  
   Abra `app/seguranca.py` e altere:  
   ```python
   CHAVE_API = "sua-chave-secreta"
   ```  
   Todas as requisições devem enviar o header:  
   ```
   X-API-Key: sua-chave-secreta
   ```

5. **Banco de dados**  
   - O SQLite vai criar automaticamente o arquivo `procedimentos.db` na primeira execução.  
   - Para usar PostgreSQL ou outro SGBD, ajuste a URL em `app/database.py`.

---

## Executando localmente

```bash
uvicorn app.main:app --reload
```

- O servidor ficará disponível em `http://127.0.0.1:8000`.  
- Acesse `http://127.0.0.1:8000/docs` para a documentação interativa Swagger.

---

## Endpoints

### Procedimentos

| Método  | Rota                        | Descrição                                           |
|--------|-----------------------------|-----------------------------------------------------|
| **POST**   | `/procedimentos/`         | Cadastrar novo procedimento                         |
| **GET**    | `/procedimentos/`         | Listar procedimentos (paginação `skip`, `limit`)    |
| **GET**    | `/procedimentos/{id}`     | Obter detalhe de um procedimento                    |
| **PATCH**  | `/procedimentos/{id}`     | Atualizar status de pagamento (`?status_pagamento=`) |

### Relatórios

| Método | Rota                                                      | Descrição                                          |
|--------|-----------------------------------------------------------|----------------------------------------------------|
| **GET**    | `/relatorios/diario?dia=YYYY-MM-DD`                     | Total de procedimentos por médico em um dia         |
| **GET**    | `/relatorios/glosas?inicio=YYYY-MM-DD&fim=YYYY-MM-DD`  | Quantidade e valor total de glosas em um período    |
| **GET**    | `/relatorios/financeiro?medico_id=1`                   | Soma de valores por médico                         |

---

## Documentação e Testes

- **Swagger UI**: `GET /docs` — interface para testar todos os endpoints.  
- **Authorize**: clique em “Authorize” e informe o `X-API-Key`.  
- **Testes com curl** ou Postman, por exemplo:

  ```bash
  curl -X POST "http://127.0.0.1:8000/procedimentos/"     -H "Content-Type: application/json"     -H "X-API-Key: sua-chave-secreta"     -d '{
          "medico_id": 1,
          "paciente_id": 42,
          "data_procedimento": "2025-04-21",
          "valor_procedimento": 150.0,
          "status_pagamento": "pendente"
        }'
  ```

---

## Tratamento de erros e exceções

1. **Validação de dados (Pydantic)**  
   - Erros de schema → **422 Unprocessable Entity**  
   ```json
   {
     "detail": [
       { "loc": ["body","campo"], "msg": "...", "type": "..." }
     ]
   }
   ```

2. **API Key inválida ou ausente**  
   - **403 Forbidden**  
   ```json
   { "detail": "Chave de API inválida" }
   ```

3. **Recurso não encontrado**  
   - **404 Not Found**  
   ```json
   { "detail": "Procedimento não encontrado" }
   ```

4. **Erros gerais não capturados**  
   - **500 Internal Server Error** (padrão do FastAPI)

---

## Segurança dos dados

1. **Autenticação via API Key**  
   - Todas as rotas dependem de `verificar_chave` em `app/seguranca.py`.

2. **Validação de entrada com Pydantic**  
   - Garante tipos e formatos corretos, evita payloads malformados.

3. **ORM com SQLAlchemy**  
   - Queries parametrizadas previnem SQL injection.

4. **Tratamento de exceções controlado**  
   - Ninguém vê stack traces em produção — apenas mensagens padronizadas.

5. **HTTPS em produção**  
   - Rode atrás de nginx/Traefik com certificado TLS para proteger headers e corpo das requisições.

6. **Permissões de BD**  
   - Use credenciais de leitura/gravação limitadas no SGBD.

7. **Boas práticas adicionais**  
   - Rate limiting, CORS restrito, logs de auditoria.

---
