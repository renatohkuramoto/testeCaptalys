from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .models.model import Base
from .database import session_local, engine
from .routers.user import router as GitRouter

Base.metadata.create_all(bind=engine)

# Definindo tags URL Swagger
tags_metadata = [
    {
        "name": "User",
        "description": "Realiza a consulta dos dados de um usuário GitHub, local ou via API",
    }
]

app = FastAPI(
    title="Desafio técnico Captalys",
    description="O objeto deste desafio e criar uma API REST que se comunica com a API REST oficial do Github: https://api.github.com/",
    version="1.0.0",
    openapi_tags=tags_metadata
)


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(GitRouter, tags=["User"], prefix="/repositories")