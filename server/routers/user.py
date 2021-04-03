from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session

from server.database import session_local
from server.git_api.git_api import GitApi
from server.infra import infra
from server.schemas.schemas import (
    ResponseModel,
    UserSchema
)

# Dependências
def conn_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()

router = APIRouter()


@router.get("/{username}", response_description="Retorna dados do usuário GitHub")
async def get_user_data(username: str, from_local: Optional[bool] = None, db: Session = Depends(conn_db)):
    response = {}
    if from_local is None or from_local == False:
        git_user = GitApi(username)
        response = git_user.get_user_info()
        if response:
            return ResponseModel(response, "Dados do usuario retornados com sucesso.")
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    elif (from_local == True):
        response = infra.get_user_data(db, username)
        if response:
            return ResponseModel(response, "Dados local do usuario retornados com sucesso")
    raise HTTPException(status_code=404, detail="Usuario nao encontrado na base local")

@router.get("/{username}/{repository_name}", response_description="Retorna os dados do repositorio do usuario")
async def get_repository_data(username: str,
                            repository_name: str,
                            from_local: Optional[bool] = None,
                            save_data: Optional[bool] = None,
                            db: Session = Depends(conn_db)
                            ):
    response = {}
    if from_local is None or from_local == False:
        git_user = GitApi(username)
        user_data = git_user.get_user_info()
        repositories = git_user.return_repositories_data()
        response = GitApi.get_repository_info(repositories, repository_name)
        if response:
            if save_data == True:
                user_db = infra.get_user_data(db, username)
                if user_db:
                    updated_user = infra.update_user_data(db, user_db, user_data, repositories)
                    if updated_user:
                        return ResponseModel(response, "Dados do repositorio e usuario atualizados e retornados com sucesso")
                    raise HTTPException(status_code=400, detail="Dados do repositorio e usuario nao atualizados")
                else:
                    inserted = infra.save_user_data(db, user_data, repositories)
                    if inserted:
                        return ResponseModel(response, "Dados do repositorio salvo com sucesso")
                    raise HTTPException(status_code=404, detail="Erro ao salvar dados do repositorio")
            return ResponseModel(response, "Dados do repositorio retornados com sucesso")
        else:
            user_db = infra.get_user_data(db, username)
            if user_db:
                    updated_user = infra.update_user_data(db, user_db, user_data, repositories)
            raise HTTPException(status_code=404, detail="Repositorio nao encontrado")
    else:
        response = infra.get_repository_user(db, repository_name)
        if response:
            return ResponseModel(response, "Dados local do repositorio retornado com sucesso")
        raise HTTPException(status_code=404, detail="Repositorio nao encontrado na base local")
