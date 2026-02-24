import requests

hearder = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzcyMTM3NDI4fQ.9a0jdUFQuq7InskloDf-rDQEr0c7kf5LuB4cc4FS8N8"
}

requisicao = requests.get("http://localhost:8000/auth/refresh", headers=hearder)
print(requisicao.json())