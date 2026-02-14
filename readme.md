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