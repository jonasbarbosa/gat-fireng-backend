# GAT Fireng - Backend

Backend do sistema GAT Fireng (Gestão de Atendimento Técnico) desenvolvido em Flask + Python.

## 🚀 Deploy na Vercel

### Pré-requisitos
- Conta na Vercel
- Repositório GitHub conectado
- Banco de dados configurado

### Configuração

1. **Conectar Repositório**
   - Acesse [vercel.com](https://vercel.com)
   - Importe este repositório
   - Configure o diretório raiz como `.` (raiz do projeto)

2. **Variáveis de Ambiente**
   - `DATABASE_URL`: URL do banco de dados (ex: mysql://user:pass@host:port/db)
   - `JWT_SECRET_KEY`: Chave secreta para JWT (ex: sua-chave-super-secreta)
   - `CORS_ORIGINS`: URLs permitidas para CORS (ex: https://gat-fireng-frontend.vercel.app)

3. **Deploy Automático**
   - Push para `main` = deploy automático
   - Pull Requests = deploy de preview

### Estrutura do Projeto

```
├── api/                    # Serverless Functions
│   ├── app.py             # Aplicação Flask principal
│   ├── config.py          # Configurações
│   ├── decorators.py      # Decorators de autenticação
│   ├── models/            # Modelos SQLAlchemy
│   ├── routes/            # Rotas da API
│   ├── requirements.txt    # Dependências Python
│   └── index.py           # Entry point para Vercel
├── vercel.json            # Configuração Vercel
└── README.md              # Este arquivo
```

### Tecnologias

- **Flask 3.0** (Framework web)
- **SQLAlchemy** (ORM)
- **Flask-JWT-Extended** (Autenticação)
- **Flask-CORS** (CORS)
- **Flasgger** (Documentação Swagger)
- **PyMySQL** (Driver MySQL)
- **bcrypt** (Hash de senhas)

### API Endpoints

#### **Autenticação**
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Renovar token
- `POST /api/auth/logout` - Logout

#### **Usuários**
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `PUT /api/users/<id>` - Atualizar usuário
- `DELETE /api/users/<id>` - Excluir usuário

#### **Técnicos**
- `GET /api/users/technicians` - Listar técnicos
- `POST /api/users/technicians` - Criar técnico
- `PUT /api/users/technicians/<id>` - Atualizar técnico

#### **Equipes**
- `GET /api/teams` - Listar equipes
- `POST /api/teams` - Criar equipe
- `PUT /api/teams/<id>` - Atualizar equipe
- `DELETE /api/teams/<id>` - Excluir equipe

#### **Inspeções**
- `GET /api/inspections` - Listar inspeções
- `POST /api/inspections` - Criar inspeção
- `PUT /api/inspections/<id>` - Atualizar inspeção
- `DELETE /api/inspections/<id>` - Excluir inspeção

#### **Manutenções**
- `GET /api/maintenances` - Listar manutenções
- `POST /api/maintenances` - Criar manutenção
- `PUT /api/maintenances/<id>` - Atualizar manutenção

#### **Clientes**
- `GET /api/clients` - Listar clientes
- `POST /api/clients` - Criar cliente
- `PUT /api/clients/<id>` - Atualizar cliente

#### **Equipamentos**
- `GET /api/equipments` - Listar equipamentos
- `POST /api/equipments` - Criar equipamento
- `PUT /api/equipments/<id>` - Atualizar equipamento

### Documentação da API

Acesse `/api/docs` para ver a documentação interativa Swagger.

### Variáveis de Ambiente

```bash
# Desenvolvimento local (.env)
DATABASE_URL=mysql://user:pass@localhost:3306/fireng
JWT_SECRET_KEY=sua-chave-super-secreta
CORS_ORIGINS=http://localhost:5173

# Produção (Vercel)
DATABASE_URL=mysql://user:pass@host:port/db
JWT_SECRET_KEY=sua-chave-super-secreta-producao
CORS_ORIGINS=https://gat-fireng-frontend.vercel.app
```

### Desenvolvimento Local

```bash
# Instalar dependências
pip install -r api/requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env

# Executar aplicação
python api/app.py
```

### Banco de Dados

O sistema usa MySQL/MariaDB. Configure a URL de conexão na variável `DATABASE_URL`.

### Autenticação

- **JWT Tokens**: Access token (15 min) + Refresh token (7 dias)
- **Roles**: superadmin, admin, coord, tecnico, cliente
- **Middleware**: `@jwt_required()` e `@role_required()`

### CORS

Configurado para aceitar requisições do frontend. URLs permitidas configuradas via `CORS_ORIGINS`.

### Monitoramento

- **Logs**: Disponíveis no dashboard da Vercel
- **Métricas**: Performance e uso em tempo real
- **Health Check**: `GET /api/health`

### Suporte

Para dúvidas sobre o deploy, consulte a [documentação da Vercel](https://vercel.com/docs).

### Licença

MIT License - veja o arquivo LICENSE para detalhes.