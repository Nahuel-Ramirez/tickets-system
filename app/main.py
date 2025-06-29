from fastapi import FastAPI
from app.routes import tickets, usuarios, auth

app = FastAPI()

app.include_router(tickets.router)
app.include_router(usuarios.router)
app.include_router(auth.router)
