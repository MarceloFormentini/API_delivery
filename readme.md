# Backend com FastAPI
Foi desenvolvido um backend para registrar pedidos de um delivery

Deve ser instalado os pacotes
```
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart
```

Para rodar o projeto execute o comando:
```
uvicorn main:app --reload
```


Padrão Rest APIs
GET -> leitura/pegar
POST -> Enviar/criar
PUT/PATCH -> edição (um registro ou vários)
DELETE -> deletar

Gerar arquivo de migração
```
alembic revision --autogenerate -m "Initial migration"
```

Executar o arquivo de migração 
```
alembic upgrade head
```

O access_token tem duração de 30 minutos, o refresh_token tem duração de 7 dias. Quando vence o access_token é feita uma requisição com o refresh_token e é gerado um novo access_token que será usado para as novas requisições.

Passado esses 7 dias, obriga a informar usuário e senha para ser gerado novos tokens.