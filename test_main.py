from fastapi.testclient import TestClient
from server.app import app
import shutil
import os

os.remove("database.db")
shutil.copy("server/database_test/database.db", "database.db")

client = TestClient(app)

def test_get_user_data_api():
    response = client.get("/repositories/renatohkuramoto")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "user_id": 62068687,
                "username": "renatohkuramoto",
                "repositories": [
                    "api-python-simple-exemple",
                    "apiDreamTeam",
                    "appSystemATT",
                    "flask-dashboard",
                    "integration-pipedrive-bling",
                    "python-tkinter",
                    "testeCaptalys"
                    ]
                }
            ],
        "code": 200,
        "message": "Dados do usuario retornados com sucesso."
    }


def test_invalid_get_user_data_api():
    response = client.get("/repositories/renatohkuramot0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuario nao encontrado"
        }

    
def test_get_repositiry_data_api_save():
    response = client.get("/repositories/renatohkuramoto/testeCaptalys?save_data=true")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "repo_id": 353874966,
                "url": "https://github.com/renatohkuramoto/testeCaptalys",
                "name": "testeCaptalys",
                "access_type": "public",
                "created_at": "2021-04-02T01:50:48Z",
                "updated_at": "2021-04-02T01:50:48Z",
                "size": 0,
                "stargazers_count": 0,
                "watchers_count": 0
                }
            ],
        "code": 200,
        "message": "Dados do repositorio salvo com sucesso"
    }


def test_invalid_get_repositiry_data_api():
    response = client.get("/repositories/renatohkuramoto/repoFalse")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Repositorio nao encontrado"
        }


def test_get_user_data_local():
    response = client.get("/repositories/renatohkuramoto?from_local=true")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "username": "renatohkuramoto",
                "id": 1,
                "repositories": [
                    "api-python-simple-exemple",
                    "apiDreamTeam",
                    "appSystemATT",
                    "flask-dashboard",
                    "integration-pipedrive-bling",
                    "python-tkinter",
                    "testeCaptalys"
                    ],
                "user_id": 62068687
                }
            ],
        "code": 200,
        "message": "Dados local do usuario retornados com sucesso"
    }


def test_invalid_get_user_data():
    response = client.get("/repositories/renatohkuramot0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuario nao encontrado"
        }


def test_get_repository_data_local():
    response = client.get("/repositories/renatohkuramoto/testeCaptalys?from_local=true")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            [
                {
                    "stargazers_count": 0,
                    "updated_at": "2021-04-02T01:50:48Z",
                    "access_type": "public",
                    "url": "https://github.com/renatohkuramoto/testeCaptalys",
                    "user_id": 1,
                    "id": 7,
                    "watchers_count": 0,
                    "size": 0,
                    "created_at": "2021-04-02T01:50:48Z",
                    "name": "testeCaptalys",
                    "repo_id": 353874966
                    }
                ]
            ],
        "code": 200,
        "message": "Dados local do repositorio retornado com sucesso"
    }

def test_invalid_get_repositiry_data_local():
    response = client.get("/repositories/renatohkuramoto/repoFalse?from_local=true")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Repositorio nao encontrado na base local"
        }
