# Avito API на Python



```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```



- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

CRUD-примеры

Создание объявления через Swagger 

```bash
curl -X POST http://127.0.0.1:8000/listings \
  -H "Content-Type: application/json" \
  -d '{"title":"iPhone 15","description":"Отличное состояние","price":65000,"category":"Электроника","city":"Москва","seller_name":"Алексей"}'
```

