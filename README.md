# Central de Atendimento – API REST

Este projeto implementa uma **API REST** para distribuição de solicitações de atendimento, seguindo o desafio técnico da **Ubots / FlowPay**.

Cada solicitação é encaminhada para um dos três times de atendimento:
- **Cartões**
- **Empréstimos**
- **Outros Assuntos**

Cada atendente pode atender **até 3 clientes simultaneamente**. Caso todos os atendentes do time estejam ocupados, as solicitações ficam enfileiradas.

---

## 🚀 Como rodar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/CaMMelo/ubots-flowpay.git
cd ubots-flowpay
```

### 2. Rodar a API
```bash
docker compose up -d
```


A API estará disponível em:  
👉 `http://localhost`

A Documentação da API estará em:  
👉 `http://localhost/docs`
ou
👉 `http://localhost/redoc`

---

## 🔑 Autenticação

A autenticação é feita via **Bearer Token**.  
O token é o **UUID retornado no login**.

Exemplo de header:
```http
Authorization: Bearer <UUID_ATENDENTE>
```

---

## 📡 Endpoints

### 1. Login do atendente
```http
POST /api/login/{time}
```
- `time`: `CARTOES`, `EMPRESTIMOS` ou `OUTROS`

📌 Exemplo:
```bash
curl -X POST http://localhost/api/login/CARTOES
```

✅ Resposta:
```json
"5d6f3e38-3a13-4a40-9dcb-9f8d4c95a1c9"
```

---

### 2. Criar atendimento
```http
POST /api/atendimento
```

📌 Corpo (JSON):
```json
{
  "cliente": "João Silva",
  "mensagem": "Meu cartão não funciona",
  "assunto": "CARTOES"
}
```

📌 Exemplo:
```bash
curl -X POST http://localhost/api/atendimento   -H "Content-Type: application/json"   -d '{"cliente":"João Silva","mensagem":"Meu cartão não funciona","assunto":"CARTOES"}'
```

✅ Resposta:
```json
{
  "id": "1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f",
  "cliente": "João Silva",
  "mensagem": "Meu cartão não funciona",
  "assunto": "CARTOES"
}
```

---

### 3. Atender próximo da fila
```http
POST /api/atender
```

📌 Exemplo:
```bash
curl -X POST http://localhost/api/atender   -H "Authorization: Bearer 5d6f3e38-3a13-4a40-9dcb-9f8d4c95a1c9"
```

✅ Resposta:
```json
{
  "id": "1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f",
  "cliente": "João Silva",
  "mensagem": "Meu cartão não funciona",
  "assunto": "CARTOES"
}
```

---

### 4. Finalizar atendimento
```http
POST /api/finalizar/{id}
```

📌 Exemplo:
```bash
curl -X POST http://localhost/api/finalizar/1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f   -H "Authorization: Bearer 5d6f3e38-3a13-4a40-9dcb-9f8d4c95a1c9"
```

✅ Resposta:
```json
{
  "id": "1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f",
  "cliente": "João Silva",
  "mensagem": "Meu cartão não funciona",
  "assunto": "CARTOES"
}
```

---

### 5. Listar atendimentos ativos do atendente
```http
GET /api/atendendo
```

📌 Exemplo:
```bash
curl -X GET http://localhost/api/atendendo   -H "Authorization: Bearer 5d6f3e38-3a13-4a40-9dcb-9f8d4c95a1c9"
```

✅ Resposta:
```json
{
  "1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f": {
    "id": "1f8a1e22-3c6b-4c4f-8f3b-d7fa97e2b63f",
    "cliente": "João Silva",
    "mensagem": "Meu cartão não funciona",
    "assunto": "CARTOES"
  }
}
```
