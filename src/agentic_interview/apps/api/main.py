from fastapi import FastAPI
from apps.api.main import interviews

app = FastAPI(title="Interview Agent API")

app.include_router(interviews.router)
