# Tasks API (FastAPI)

A minimal FastAPI service providing CRUD for tasks with statuses.

## Requirements
- Python 3.13+

## Setup
You can use a virtual environment or install with user site packages.

```bash
# Option A: venv (preferred if available)
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# Option B: managed envs (use override flag)
pip install --break-system-packages -r requirements.txt --user
```

## Run the app
```bash
uvicorn app.main:app --reload
```

Then open Swagger UI at `http://localhost:8000/docs`.

## API Endpoints
- POST `/tasks`
- GET `/tasks/{id}`
- GET `/tasks?offset=&limit=`
- PUT `/tasks/{id}`
- DELETE `/tasks/{id}`

## Tests
```bash
pytest -q
```

## Docker (optional)
```bash
# Build
docker build -t tasks-api .
# Run
docker run -p 8000:8000 tasks-api
```
