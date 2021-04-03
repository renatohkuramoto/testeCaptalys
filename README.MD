# Desafio técnico Captalys
## Developer BackEnd
O objeto deste desafio e criar uma API REST que se comunica com a API REST oficial do Github: https://api.github.com/


## Instalação

Instalar os pacotes do requirements.txt

```sh
./teste_captalys
pip install -r requirements.txt
```

## Execução

```sh
./teste_captalys
python main.py
```
Por padrão a aplicação irá subir no IP 127.0.0.1 porta 8000

```sh
http://127.0.0.1:8000
```

## Rotas

### Swagger
```sh
http://127.0.0.1:8000/docs
```

### Retornar dados do usuário
Parâmetro opcional (from_local=true ou false)
```sh
http://127.0.0.1:8000/repositories/{username}
http://127.0.0.1:8000/repositories/{username}?from_local=true
```
Retorno esperado:
```sh
On Success
{
  "data": [
    {
      "user_id": 1234,
      "username": "git_username",
      "repositories": ["List repositories"]
    }
  ],
  "code": 200,
  "message": ""
}

On Fail - 404
{
  "detail": "Usuario nao encontrado"
}
```

### Retornar dados do repositório
Parâmetro opcional from_local=true ou false (Retorna dados da base local)
Parâmetro opcional save_data=true ou false (Salva os dados do usuário e repositórios)
Parâmetro save_data=true, insere, atualiza e deleta as informções do repositório na base local conforme os dados do GitHub API.

```sh
http://127.0.0.1:8000/repositories/{username}/{repository_name}
http://127.0.0.1:8000/repositories/{username}/{repository_name}?from_local=true
http://127.0.0.1:8000/repositories/{username}/{repository_name}?save_data=true
```
Retorno esperado:
```sh
On Success
{
  "data": [
    {
      "repo_id": 1234,
      "url": "URL",
      "name": "repository_name",
      "access_type": "type",
      "created_at": "Data",
      "updated_at": "Data",
      "size": 0,
      "stargazers_count": 0,
      "watchers_count": 0
    }
  ],
  "code": 200,
  "message": ""
}

On Fail - 404
{
  "detail": "Repositorio nao encontrado"
}
```

## Testes

```sh
./teste_captalys
pytest test_main.py
```



**Renato Kuramoto**