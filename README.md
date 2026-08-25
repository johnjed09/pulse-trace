### Running Local

1. Run Docker Postgres Container

```bash
docker start pulse-postgres
```

2. Activate Virtual Environment

```bash
source venv/bin/activate
```

3. Run server

```bash
uvicorn main:app --reload
```
