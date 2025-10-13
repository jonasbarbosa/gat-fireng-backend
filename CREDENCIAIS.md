# 🔐 Credenciais de Acesso - Sistema Fireng

## 📊 Resumo dos Dados

- **8 usuários** criados
- **3 equipes** técnicas
- **4 técnicos** com certificações
- **4 empresas** clientes
- **5 filiais**
- **5 contratos**
- **6 normas** técnicas

---

## 👤 Credenciais de Login

### 🔴 Super Admin
```
Email: admin@fireng.com
Senha: admin123
Role: superadmin
```

### 🟡 Coordenadores
```
Email: coord1@fireng.com
Senha: coord123
Nome: Maria Silva
Role: coord

Email: coord2@fireng.com
Senha: coord123
Nome: João Santos
Role: coord
```

### 🟢 Técnicos
```
Email: tecnico1@fireng.com
Senha: tecnico123
Nome: Carlos Oliveira
Matrícula: TEC-001
Equipe: Equipe Alpha
Especialização: Extintores, Hidrantes, Mangueiras

Email: tecnico2@fireng.com
Senha: tecnico123
Nome: Ana Paula
Matrícula: TEC-002
Equipe: Equipe Alpha
Especialização: Sistemas de Alarme, Detecção de Fumaça

Email: tecnico3@fireng.com
Senha: tecnico123
Nome: Roberto Lima
Matrícula: TEC-003
Equipe: Equipe Beta
Especialização: Sprinklers, Bombas, Manutenção Corretiva

Email: tecnico4@fireng.com
Senha: tecnico123
Nome: Fernanda Costa
Matrícula: TEC-004
Equipe: Equipe Gamma
Especialização: Instalação, Projetos, Laudos Técnicos
```

### 🔵 Cliente
```
Email: cliente1@empresa.com
Senha: cliente123
Nome: Pedro Martins
Role: cliente
```

---

## 🏢 Empresas Cadastradas

### 1. Shopping Center Paulista
- **CNPJ**: 12.345.678/0001-90
- **Contato**: Ricardo Almeida
- **Filiais**: 
  - Shopping Paulista - Torre Norte
  - Shopping Paulista - Torre Sul
- **Contrato**: CTR-2025-001 (Ativo)

### 2. Hospital São Lucas
- **CNPJ**: 23.456.789/0001-01
- **Contato**: Dra. Juliana Mendes
- **Filiais**:
  - Hospital São Lucas - Unidade Principal
- **Contrato**: CTR-2025-002 (Ativo)

### 3. Condomínio Residencial Vista Verde
- **CNPJ**: 34.567.890/0001-12
- **Contato**: Marcos Ferreira (Síndico)
- **Filiais**:
  - Condomínio Vista Verde - Bloco A
- **Contrato**: CTR-2025-003 (Ativo)

### 4. Indústria Metalúrgica ABC
- **CNPJ**: 45.678.901/0001-23
- **Contato**: Eng. Paulo Rodrigues
- **Filiais**:
  - Metalúrgica ABC - Planta 1
- **Contratos**: 
  - CTR-2024-099 (Expirado)
  - CTR-2025-004 (Ativo)

---

## 📋 Normas Técnicas Cadastradas

1. **NBR 12962** - Extintores de incêndio (2016)
2. **NBR 13714** - Sistema de hidrantes e mangotinhos (2000)
3. **NBR 17240** - Sistema de detecção e alarme (2010)
4. **NBR 10897** - Sistema de sprinklers (2020)
5. **NR 23** - Proteção contra incêndios (2011)
6. **IT 22** - Sistema de hidrantes (2019)

---

## 🚀 Como Testar

### 1. Login via API (curl)
```bash
curl -X POST 'http://localhost:5000/api/auth/login' \
  -H 'Content-Type: application/json' \
  --data-raw '{"email":"admin@fireng.com","password":"admin123"}'
```

### 2. Login via Frontend
1. Acesse: http://localhost:3000
2. Use as credenciais acima
3. Explore o dashboard

### 3. Swagger UI
1. Acesse: http://localhost:5000/api/docs
2. Faça login com qualquer credencial
3. Teste os endpoints

---

## 📊 Endpoints Principais

### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Renovar token
- `GET /api/auth/me` - Usuário atual

### GAT (Gestão)
- `GET /api/users` - Listar usuários
- `GET /api/clients` - Listar empresas
- `GET /api/branches` - Listar filiais
- `GET /api/contracts` - Listar contratos
- `GET /api/teams` - Listar equipes
- `GET /api/technicians` - Listar técnicos
- `GET /api/standards` - Listar normas

### DAT (Campo)
- `GET /api/inspections` - Listar inspeções
- `GET /api/maintenances` - Listar manutenções

---

## 🔒 Níveis de Acesso

| Role | Descrição | Permissões |
|------|-----------|------------|
| `superadmin` | Super Administrador | Acesso total ao sistema |
| `admin` | Administrador | Gerenciar tudo exceto superadmin |
| `coord` | Coordenador | Gerenciar operações e equipes |
| `tecnico` | Técnico de Campo | Inspeções e manutenções |
| `cliente` | Cliente | Visualizar seus próprios dados |

---

## 📝 Notas Importantes

1. **Senha Padrão**: Todas as senhas de teste são simples para facilitar os testes
2. **Dados de Exemplo**: Todos os dados são fictícios para demonstração
3. **Token JWT**: Válido por 24 horas (access) e 30 dias (refresh)
4. **CORS**: Configurado para aceitar http://localhost:3000

---

## 🆘 Problemas Comuns

### Erro: "Credenciais inválidas"
- Verifique se está usando o email correto: `admin@fireng.com` (não `admin@gatfireng.com`)
- Verifique se a senha está correta: `admin123`
- Execute novamente o script: `python3 create_admin_user.py`

### Erro: "Token inválido"
- Faça login novamente para obter um novo token
- Verifique se o token está sendo enviado no header: `Authorization: Bearer {token}`

### Erro: "MySQL server has gone away"
- O servidor foi reiniciado? Execute: `python3 app.py`
- Conexão está configurada corretamente no `.env`?

---

**Última atualização**: 06/10/2025 10:05 AM

