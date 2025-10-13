# 🚀 API Fireng - Documentação Completa

## 📊 Visão Geral

API REST completa para os sistemas **GAT** (Gestão de Atendimento Técnico) e **DAT** (Diário de Atendimento Técnico).

- **Base URL**: `http://localhost:5000/api`
- **Documentação Swagger**: `http://localhost:5000/api/docs`
- **Autenticação**: JWT Bearer Token
- **Formato**: JSON

---

## 🔐 Autenticação (Compartilhado)

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| POST | `/auth/register` | Registrar novo usuário | Público |
| POST | `/auth/login` | Login e obter tokens | Público |
| POST | `/auth/refresh` | Renovar access token | JWT |
| GET | `/auth/me` | Dados do usuário atual | JWT |
| PUT | `/auth/change-password` | Alterar senha | JWT |

---

## 👥 GAT - Gestão de Usuários

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/users` | Listar usuários | Admin, Coord |
| POST | `/users` | Criar usuário | Admin |
| GET | `/users/{id}` | Detalhes do usuário | Admin, Coord |
| PUT | `/users/{id}` | Atualizar usuário | Admin |
| DELETE | `/users/{id}` | Excluir usuário | SuperAdmin |

**Roles**: `superadmin`, `admin`, `coord`, `tecnico`, `cliente`

---

## 🏢 GAT - Empresas (Clientes)

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/clients` | Listar empresas | Admin, Coord |
| POST | `/clients` | Criar empresa | Admin, Coord |
| GET | `/clients/{id}` | Detalhes da empresa | Admin, Coord, Técnico |
| PUT | `/clients/{id}` | Atualizar empresa | Admin, Coord |
| DELETE | `/clients/{id}` | Excluir empresa | SuperAdmin, Admin |

**Filtros**: `?is_active=true`

---

## 🏢 GAT - Filiais

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/branches` | Listar filiais | Admin, Coord |
| POST | `/branches` | Criar filial | Admin, Coord |
| GET | `/branches/{id}` | Detalhes da filial | Admin, Coord, Técnico |
| PUT | `/branches/{id}` | Atualizar filial | Admin, Coord |
| DELETE | `/branches/{id}` | Excluir filial | SuperAdmin, Admin |

**Filtros**: `?company_id=1&is_active=true`

**Campos**:
- `name` (obrigatório)
- `cnpj` (único)
- `address`, `city`, `state`, `zip_code`
- `phone`, `email`
- `company_id` (obrigatório)
- `notes`

---

## 📄 GAT - Contratos

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/contracts` | Listar contratos | Admin, Coord |
| POST | `/contracts` | Criar contrato | Admin, Coord |
| GET | `/contracts/{id}` | Detalhes do contrato | Admin, Coord, Técnico |
| PUT | `/contracts/{id}` | Atualizar contrato | Admin, Coord |
| DELETE | `/contracts/{id}` | Excluir contrato | SuperAdmin, Admin |

**Filtros**: `?company_id=1&status=ativo`

**Status**: `ativo`, `inativo`, `expirado`, `suspenso`

**Campos**:
- `contract_number` (obrigatório, único)
- `description`
- `start_date`, `end_date` (obrigatórios)
- `status`, `value`
- `company_id` (obrigatório)
- `branch_id`, `team_id`

---

## 👥 GAT - Equipes

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/teams` | Listar equipes | Admin, Coord |
| POST | `/teams` | Criar equipe | Admin, Coord |
| GET | `/teams/{id}` | Detalhes da equipe | Admin, Coord, Técnico |
| PUT | `/teams/{id}` | Atualizar equipe | Admin, Coord |
| DELETE | `/teams/{id}` | Excluir equipe | SuperAdmin, Admin |

**Filtros**: `?is_active=true`

**Campos**:
- `name` (obrigatório, único)
- `description`

---

## 🔧 GAT - Técnicos

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/technicians` | Listar técnicos | Admin, Coord |
| POST | `/technicians` | Criar perfil técnico | Admin, Coord |
| GET | `/technicians/{id}` | Detalhes do técnico | Admin, Coord, Técnico |
| PUT | `/technicians/{id}` | Atualizar técnico | Admin, Coord |
| DELETE | `/technicians/{id}` | Excluir técnico | SuperAdmin, Admin |

**Filtros**: `?team_id=1&is_available=true`

**Campos**:
- `user_id` (obrigatório, único)
- `registration_number` (único)
- `specialty`
- `team_id`
- `is_available`

---

## 📋 GAT - Normas Técnicas

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/standards` | Listar normas | Admin, Coord, Técnico |
| POST | `/standards` | Criar norma | Admin, Coord |
| GET | `/standards/{id}` | Detalhes da norma | Admin, Coord, Técnico |
| PUT | `/standards/{id}` | Atualizar norma | Admin, Coord |
| DELETE | `/standards/{id}` | Excluir norma | SuperAdmin, Admin |

**Filtros**: `?is_active=true`

**Exemplos de Normas**:
- NBR 12962 - Extintores de incêndio
- IT 17 - Sistema de hidrantes e mangotinhos
- NR 23 - Proteção contra incêndios

**Campos**:
- `name` (obrigatório, único)
- `code` (obrigatório, único)
- `description`

---

## 📦 GAT - Inventários

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/inventories` | Listar inventários | Admin, Coord, Técnico |
| POST | `/inventories` | Criar inventário | Admin, Coord |
| GET | `/inventories/{id}` | Detalhes do inventário | Admin, Coord, Técnico |
| PUT | `/inventories/{id}` | Atualizar inventário | Admin, Coord |
| DELETE | `/inventories/{id}` | Excluir inventário | SuperAdmin, Admin |

**Filtros**: `?branch_id=1`

**Regra**: Cada filial possui apenas 1 inventário

**Campos**:
- `name` (obrigatório)
- `description`
- `branch_id` (obrigatório, único)

---

## 🧯 GAT - Equipamentos

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/equipments` | Listar equipamentos | Admin, Coord, Técnico |
| POST | `/equipments` | Criar equipamento | Admin, Coord |
| GET | `/equipments/{id}` | Detalhes do equipamento | Admin, Coord, Técnico |
| PUT | `/equipments/{id}` | Atualizar equipamento | Admin, Coord |
| DELETE | `/equipments/{id}` | Excluir equipamento | SuperAdmin, Admin |

**Filtros**: `?inventory_id=1&is_active=true`

**Campos**:
- `name` (obrigatório)
- `serial_number` (obrigatório, único)
- `model`, `manufacturer`
- `installation_date`, `last_maintenance_date`, `next_maintenance_date`
- `location_description`
- `inventory_id` (obrigatório)
- `standard_ids` (array) - Normas aplicáveis
- `notes`

**Relacionamento N:N**: Um equipamento pode ter várias normas

---

## 📋 DAT - Inspeções

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/inspections` | Listar inspeções | Admin, Coord, Técnico |
| POST | `/inspections` | Criar inspeção | Admin, Coord, Técnico |
| GET | `/inspections/{id}` | Detalhes da inspeção | Admin, Coord, Técnico |
| PUT | `/inspections/{id}` | Atualizar inspeção | Admin, Coord, Técnico |
| DELETE | `/inspections/{id}` | Excluir inspeção | SuperAdmin, Admin |

**Filtros**: `?client_id=1&status=concluida&technician_id=2`

**Status**: `pendente`, `em_andamento`, `concluida`, `cancelada`

**Campos Principais**:
- `title`, `description`
- `scheduled_date`, `completed_date`
- `status`, `priority`
- `location`, `equipment`
- `client_id`, `technician_id`, `created_by`
- `branch_id`, `equipment_id`, `contract_id`, `team_id`
- `findings`, `recommendations`
- `photos`, `signature`

---

## 🔧 DAT - Manutenções

### Endpoints

| Método | Endpoint | Descrição | Acesso |
|--------|----------|-----------|--------|
| GET | `/maintenances` | Listar manutenções | Admin, Coord, Técnico |
| POST | `/maintenances` | Criar manutenção | Admin, Coord, Técnico |
| GET | `/maintenances/{id}` | Detalhes da manutenção | Admin, Coord, Técnico |
| PUT | `/maintenances/{id}` | Atualizar manutenção | Admin, Coord, Técnico |
| DELETE | `/maintenances/{id}` | Excluir manutenção | SuperAdmin, Admin |

**Filtros**: `?client_id=1&status=concluida&maintenance_type=preventiva`

**Status**: `agendada`, `em_andamento`, `concluida`, `cancelada`

**Tipos**: `preventiva`, `corretiva`, `emergencial`, `instalacao`

**Campos Principais**:
- `title`, `description`
- `maintenance_type`
- `scheduled_date`, `completed_date`
- `status`, `priority`
- `location`, `equipment`
- `client_id`, `technician_id`, `created_by`
- `branch_id`, `equipment_id`, `contract_id`, `team_id`
- `work_performed`, `parts_used`, `observations`
- `photos`, `signature`
- `labor_cost`, `parts_cost`, `total_cost`

---

## 🔒 Segurança

### Autenticação JWT

```bash
# 1. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@fireng.com", "password": "admin123"}'

# Resposta:
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "user": {...}
}

# 2. Usar token nas requisições
curl -X GET http://localhost:5000/api/clients \
  -H "Authorization: Bearer eyJhbGc..."
```

### Níveis de Acesso

| Role | Descrição | Permissões |
|------|-----------|------------|
| `superadmin` | Super administrador | Acesso total |
| `admin` | Administrador | Gerenciar tudo exceto superadmin |
| `coord` | Coordenador | Gerenciar operações e visualizar relatórios |
| `tecnico` | Técnico de campo | Criar/editar inspeções e manutenções |
| `cliente` | Cliente | Visualizar seus próprios dados |

---

## 📊 Modelo de Dados (UML)

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Client    │──1:N──│   Branch    │──1:1──│  Inventory  │
│  (Empresa)  │       │  (Filial)   │       │             │
└─────────────┘       └─────────────┘       └─────────────┘
      │                      │                      │
      │                      │                      │
      │                      │                      │1:N
      │                      │                      │
      │                      │               ┌─────────────┐
      │                      │               │  Equipment  │
      │                      │               │             │
      │                      │               └─────────────┘
      │                      │                      │N:N
      │                      │                      │
      │                      │               ┌─────────────┐
      │                      │               │  Standard   │
      │                      │               │  (Normas)   │
      │                      │               └─────────────┘
      │                      │
      │1:N                   │1:N
      │                      │
┌─────────────┐       ┌─────────────┐
│  Contract   │       │    Team     │
│             │       │             │
└─────────────┘       └─────────────┘
      │                      │1:N
      │                      │
      │                ┌─────────────┐
      │                │ Technician  │
      │                │             │
      │                └─────────────┘
      │                      │
      │                      │
      │                      │
┌─────────────────────────────────────┐
│         Inspection / Maintenance     │
│  (Relaciona: Client, Branch,         │
│   Equipment, Contract, Team,         │
│   Technician)                        │
└─────────────────────────────────────┘
```

---

## 🧪 Exemplos de Uso

### 1. Criar uma Empresa com Filial

```bash
# 1. Criar empresa
curl -X POST http://localhost:5000/api/clients \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Empresa XYZ Ltda",
    "cnpj": "12.345.678/0001-90",
    "email": "contato@xyz.com",
    "phone": "(11) 1234-5678"
  }'

# 2. Criar filial
curl -X POST http://localhost:5000/api/branches \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Filial São Paulo",
    "cnpj": "12.345.678/0002-71",
    "company_id": 1,
    "address": "Av. Paulista, 1000",
    "city": "São Paulo",
    "state": "SP"
  }'
```

### 2. Criar Contrato com Equipe

```bash
# 1. Criar equipe
curl -X POST http://localhost:5000/api/teams \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Equipe Alpha",
    "description": "Equipe especializada em manutenção preventiva"
  }'

# 2. Criar contrato
curl -X POST http://localhost:5000/api/contracts \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contract_number": "CTR-2025-001",
    "company_id": 1,
    "branch_id": 1,
    "team_id": 1,
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-12-31T23:59:59Z",
    "value": 50000.00,
    "status": "ativo"
  }'
```

### 3. Criar Inventário com Equipamentos

```bash
# 1. Criar inventário
curl -X POST http://localhost:5000/api/inventories \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inventário Filial SP",
    "branch_id": 1
  }'

# 2. Criar norma
curl -X POST http://localhost:5000/api/standards \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Extintores de incêndio",
    "code": "NBR 12962"
  }'

# 3. Criar equipamento
curl -X POST http://localhost:5000/api/equipments \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Extintor PQS 6kg",
    "serial_number": "EXT-001-2025",
    "model": "ABC-6",
    "manufacturer": "Fabricante XYZ",
    "inventory_id": 1,
    "standard_ids": [1],
    "location_description": "Corredor principal - próximo ao elevador"
  }'
```

### 4. Registrar Inspeção

```bash
curl -X POST http://localhost:5000/api/inspections \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inspeção Mensal - Janeiro 2025",
    "description": "Inspeção de rotina dos equipamentos",
    "client_id": 1,
    "branch_id": 1,
    "equipment_id": 1,
    "contract_id": 1,
    "team_id": 1,
    "technician_id": 2,
    "scheduled_date": "2025-01-15T09:00:00Z",
    "status": "pendente",
    "priority": "media"
  }'
```

---

## 📈 Estatísticas da API

- **Total de Endpoints**: 60+
- **Modelos de Dados**: 12
- **Relacionamentos**: 15+
- **Autenticação**: JWT com refresh token
- **Documentação**: Swagger/OpenAPI 2.0

---

## 🚀 Próximos Passos

1. ✅ Modelos implementados
2. ✅ Rotas CRUD completas
3. ✅ Documentação Swagger
4. ⏳ Testes automatizados
5. ⏳ Paginação e ordenação
6. ⏳ Upload de fotos
7. ⏳ Relatórios em PDF
8. ⏳ Notificações em tempo real

---

## 📞 Suporte

- **Swagger UI**: http://localhost:5000/api/docs
- **API Spec JSON**: http://localhost:5000/apispec.json

---

**Desenvolvido com ❤️ para Fireng**
