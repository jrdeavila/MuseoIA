from contextlib import asynccontextmanager, contextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from api.routes import router
from core.application.exceptions.exception import MessageException
from core.infrastructure.singleton.configure import configure_dependencies


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await configure_dependencies()
    print("Started up.")
    try:
        yield
    finally:
        print("Shutting down...")
        print("Shut down.")


app = FastAPI(
    title="Museo el Cocha Molina FastAPI",
    description="API para el Museo el Cocha Molina",
    lifespan=lifespan,
)


app.include_router(router)


@app.exception_handler(MessageException)
async def message_error_exception_handler(request, exc: MessageException):
    return JSONResponse(
        status_code=400,
        content={"message": exc.message},
        headers=exc.headers,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
