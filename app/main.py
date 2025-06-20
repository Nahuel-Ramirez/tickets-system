from fastapi import FastAPI
from app.routes import tickets

app = FastAPI()

app.include_router(tickets.router)