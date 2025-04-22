# Procedimentos Médicos API

API REST para cadastro de procedimentos médicos, relatórios de glosas e financeiros.

## Tecnologias

- Python 3.9+
- FastAPI
- SQLite + SQLAlchemy
- Swagger automático em `/docs`

## Como rodar

1. Crie e ative um virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
2. Instale as dependências
    ```bash
    pip install -r requirements.txt
3. Ajuste a chave de API (opcional) em app/dependencies.py:
    ```bash
    API_KEY = "<sua_chave>"
4. Inicie o servidor:
    ```bash
    uvicorn app.main:app --reload
5. Acesse a documentação interativa em:
    ```bash
    http://localhost:8000/docs