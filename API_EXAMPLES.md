# Exemplos de Requisições da API

Este documento contém exemplos de requisições para testar a API do Sistema Fireng.

## Base URL

```
http://localhost:5000/api
```

## Autenticação

Todas as requisições (exceto login e register) requerem o header:

```
Authorization: Bearer {access_token}
```

---

## 🔐 Autenticação

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "admin@fireng.com",
  "password": "admin123"
}
```

**Resposta:**
```json
{
  "message": "Login realizado com sucesso",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "admin@fireng.com",
    "name": "Administrador",
    "role": "superadmin",
    "is_active": true
  }
}
```

### Registrar Novo Usuário

```http
POST /api/auth/register
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "email": "tecnico@fireng.com",
  "password": "senha123",
  "name": "João Silva",
  "role": "tecnico",
  "phone": "11999999999"
}
```

### Obter Usuário Atual

```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

### Alterar Senha

```http
POST /api/auth/change-password
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "current_password": "senha_atual",
  "new_password": "nova_senha"
}
```

### Refresh Token

```http
POST /api/auth/refresh
Authorization: Bearer {refresh_token}
```

---

## 👥 Usuários

### Listar Usuários

```http
GET /api/users
Authorization: Bearer {access_token}

# Com filtros
GET /api/users?role=tecnico
GET /api/users?is_active=true
```

### Obter Usuário Específico

```http
GET /api/users/1
Authorization: Bearer {access_token}
```

### Atualizar Usuário

```http
PUT /api/users/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "João Silva Santos",
  "phone": "11988888888",
  "is_active": true
}
```

### Desativar Usuário

```http
DELETE /api/users/1
Authorization: Bearer {access_token}
```

### Listar Técnicos

```http
GET /api/users/technicians
Authorization: Bearer {access_token}
```

---

## 🏢 Clientes

### Listar Clientes

```http
GET /api/clients
Authorization: Bearer {access_token}

# Com filtros
GET /api/clients?is_active=true
GET /api/clients?search=empresa
```

### Obter Cliente Específico

```http
GET /api/clients/1
Authorization: Bearer {access_token}
```

### Criar Cliente

```http
POST /api/clients
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Empresa XYZ Ltda",
  "email": "contato@empresaxyz.com",
  "phone": "1133334444",
  "cpf_cnpj": "12345678000190",
  "address": "Rua Exemplo, 123",
  "city": "São Paulo",
  "state": "SP",
  "zip_code": "01234-567",
  "notes": "Cliente preferencial"
}
```

### Atualizar Cliente

```http
PUT /api/clients/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Empresa XYZ S.A.",
  "phone": "1133335555",
  "notes": "Cliente VIP"
}
```

### Desativar Cliente

```http
DELETE /api/clients/1
Authorization: Bearer {access_token}
```

---

## 📋 Inspeções

### Listar Inspeções

```http
GET /api/inspections
Authorization: Bearer {access_token}

# Com filtros
GET /api/inspections?status=pendente
GET /api/inspections?technician_id=2
GET /api/inspections?client_id=1
GET /api/inspections?date_from=2025-10-01T00:00:00
GET /api/inspections?date_to=2025-10-31T23:59:59
```

### Obter Inspeção Específica

```http
GET /api/inspections/1
Authorization: Bearer {access_token}
```

### Criar Inspeção

```http
POST /api/inspections
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Inspeção Preventiva - Equipamento A",
  "description": "Verificar estado geral do equipamento",
  "scheduled_date": "2025-10-15T14:00:00",
  "client_id": 1,
  "technician_id": 2,
  "priority": "alta",
  "location": "Rua Exemplo, 123 - São Paulo/SP",
  "equipment": "Equipamento A - Modelo XYZ"
}
```

### Atualizar Inspeção

```http
PUT /api/inspections/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "em_andamento",
  "observations": "Iniciando inspeção",
  "result": "Equipamento em bom estado"
}
```

### Concluir Inspeção

```http
PUT /api/inspections/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "concluida",
  "result": "Inspeção concluída com sucesso. Equipamento aprovado.",
  "observations": "Nenhuma anomalia detectada",
  "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
}
```

### Cancelar Inspeção

```http
DELETE /api/inspections/1
Authorization: Bearer {access_token}
```

---

## 🔧 Manutenções

### Listar Manutenções

```http
GET /api/maintenances
Authorization: Bearer {access_token}

# Com filtros
GET /api/maintenances?status=pendente
GET /api/maintenances?type=preventiva
GET /api/maintenances?technician_id=2
GET /api/maintenances?client_id=1
GET /api/maintenances?date_from=2025-10-01T00:00:00
GET /api/maintenances?date_to=2025-10-31T23:59:59
```

### Obter Manutenção Específica

```http
GET /api/maintenances/1
Authorization: Bearer {access_token}
```

### Criar Manutenção

```http
POST /api/maintenances
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Manutenção Preventiva - Sistema de Refrigeração",
  "description": "Troca de filtros e verificação geral",
  "maintenance_type": "preventiva",
  "scheduled_date": "2025-10-20T09:00:00",
  "client_id": 1,
  "technician_id": 2,
  "priority": "media",
  "location": "Rua Exemplo, 123 - São Paulo/SP",
  "equipment": "Sistema de Refrigeração - Modelo ABC"
}
```

### Atualizar Manutenção

```http
PUT /api/maintenances/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "em_andamento",
  "work_performed": "Iniciando troca de filtros",
  "observations": "Filtros muito sujos, necessário limpeza adicional"
}
```

### Concluir Manutenção

```http
PUT /api/maintenances/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "status": "concluida",
  "work_performed": "Troca de filtros completa. Limpeza do sistema. Verificação de pressão.",
  "parts_used": "[{\"name\": \"Filtro A\", \"quantity\": 2, \"cost\": 50.00}, {\"name\": \"Filtro B\", \"quantity\": 1, \"cost\": 80.00}]",
  "observations": "Sistema funcionando perfeitamente",
  "labor_cost": 200.00,
  "parts_cost": 180.00,
  "total_cost": 380.00,
  "signature": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA..."
}
```

### Cancelar Manutenção

```http
DELETE /api/maintenances/1
Authorization: Bearer {access_token}
```

---

## 📊 Status e Prioridades

### Status Disponíveis
- `pendente` - Aguardando execução
- `em_andamento` - Em execução
- `concluida` - Finalizada
- `cancelada` - Cancelada

### Prioridades Disponíveis
- `baixa` - Baixa prioridade
- `media` - Média prioridade
- `alta` - Alta prioridade
- `urgente` - Urgente

### Tipos de Manutenção
- `preventiva` - Manutenção preventiva
- `corretiva` - Manutenção corretiva
- `preditiva` - Manutenção preditiva

### Roles (Papéis)
- `superadmin` - Super Administrador
- `admin` - Administrador
- `coord` - Coordenador
- `tecnico` - Técnico
- `cliente` - Cliente

---

## 🧪 Testando com cURL

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@fireng.com","password":"admin123"}'
```

### Listar Inspeções
```bash
curl -X GET http://localhost:5000/api/inspections \
  -H "Authorization: Bearer {seu_token_aqui}"
```

### Criar Cliente
```bash
curl -X POST http://localhost:5000/api/clients \
  -H "Authorization: Bearer {seu_token_aqui}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Empresa Teste",
    "email": "teste@empresa.com",
    "phone": "11999999999"
  }'
```

---

## 🔍 Códigos de Resposta HTTP

- `200 OK` - Requisição bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `409 Conflict` - Conflito (ex: email já cadastrado)
- `500 Internal Server Error` - Erro no servidor

---

## 💡 Dicas

1. **Salve o token**: Após o login, salve o `access_token` para usar nas próximas requisições
2. **Refresh Token**: Use o `refresh_token` para obter um novo `access_token` quando expirar
3. **Filtros**: Combine múltiplos filtros nas requisições GET
4. **Datas**: Use formato ISO 8601 para datas: `YYYY-MM-DDTHH:mm:ss`
5. **JSON**: Sempre use `Content-Type: application/json` ao enviar dados

---

## 🛠️ Ferramentas Recomendadas

- **Postman** - Cliente HTTP com interface gráfica
- **Insomnia** - Alternativa ao Postman
- **cURL** - Linha de comando
- **HTTPie** - cURL mais amigável
- **Thunder Client** - Extensão do VS Code

