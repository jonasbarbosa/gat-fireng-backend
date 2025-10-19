# Fireng Backend - Sistema GAT & DAT

Sistema backend unificado para os aplicativos Fireng:
- **GAT (Gestão de Atendimento Técnico)**: Sistema web administrativo
- **DAT (Diário de Atendimento Técnico)**: Aplicativo mobile para técnicos

## 🚀 Execução Local

### Pré-requisitos
- Python 3.9 ou superior
- pip3 instalado

### Instalação e Execução

1. **Instalar dependências:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Executar o servidor:**
   ```bash
   python3 run_local.py
   ```

3. **Acessar a API:**
   - API: http://localhost:5001
   - Documentação Swagger: http://localhost:5001/api/docs
   - Health Check: http://localhost:5001/api/health

### Configuração

O projeto usa um arquivo `.env` para configurações. Para desenvolvimento local:
- Banco de dados: SQLite (arquivo `instance/fireng.db`)
- Ambiente: development
- Debug: habilitado

### Estrutura do Projeto

```
api/
├── app.py              # Aplicação principal Flask
├── config.py           # Configurações
├── models/             # Modelos do banco de dados
├── routes/             # Rotas da API
└── decorators.py       # Decoradores personalizados

run_local.py            # Script de execução local
requirements.txt        # Dependências Python
.env                    # Configurações de ambiente
```

### Endpoints Principais

#### Autenticação
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Registro
- `POST /api/auth/refresh` - Renovar token

#### Usuários (GAT)
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `PUT /api/users/{id}` - Atualizar usuário

#### Inspeções (DAT)
- `GET /api/inspections` - Listar inspeções
- `POST /api/inspections` - Criar inspeção
- `PUT /api/inspections/{id}` - Atualizar inspeção

#### Manutenções (DAT)
- `GET /api/maintenances` - Listar manutenções
- `POST /api/maintenances` - Criar manutenção

### Banco de Dados

O projeto suporta:
- **SQLite** (desenvolvimento local)
- **MySQL** (produção)

Para usar MySQL em desenvolvimento, modifique o arquivo `.env`:
```
USE_SQLITE=false
```

### Troubleshooting

#### Erro de imports relativos
Se encontrar erros como "attempted relative import with no known parent package":
- Use sempre `python3 run_local.py` (não execute `api/app.py` diretamente)
- O script `run_local.py` configura corretamente o Python path

#### Erro de dependências
Se alguma dependência não estiver instalada:
```bash
pip3 install -r requirements.txt
```

#### Erro de banco de dados
Se o banco SQLite não for criado automaticamente:
```bash
mkdir -p instance
```

### Desenvolvimento

Para desenvolvimento, o servidor roda com:
- Debug habilitado
- Auto-reload ativado
- Logs detalhados
- CORS configurado para localhost

### Produção

Para deploy em produção, use:
- Banco MySQL
- Variáveis de ambiente adequadas
- Configurações de segurança
- SSL/TLS habilitado
