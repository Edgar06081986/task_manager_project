from fastapi import FastAPI

from app.api.routes.tasks import router as tasks_router


def create_app() -> FastAPI:
    application = FastAPI(title="Tasks API", version="1.0.0")
    application.include_router(tasks_router)
    return application


app = create_app()