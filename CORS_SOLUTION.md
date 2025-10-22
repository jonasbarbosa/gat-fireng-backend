# Problema de CORS - Documentação e Solução

## 🚨 Problema Identificado

O frontend estava enfrentando erros de CORS ao tentar fazer requisições para o backend:

```
Access to XMLHttpRequest at 'https://gat-fireng-backend.vercel.app/api/contracts' 
from origin 'https://gat-fireng-frontend.vercel.app' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## ✅ Solução Implementada

### 1. Configuração CORS Robusta no Backend (`api/app.py`)

```python
# Configuração CORS robusta para produção e desenvolvimento
allowed_origins = [
    'https://gat-fireng-frontend.vercel.app',  # Frontend em produção
    'http://localhost:5173',                   # Vite dev server
    'http://localhost:5174',                   # Vite dev server alternativo
    'http://localhost:3000',                   # React dev server
    'http://localhost:5001'                    # Backend local
]

# Adicionar origens do arquivo de configuração
config_origins = app.config.get('CORS_ORIGINS', [])
if isinstance(config_origins, str):
    config_origins = config_origins.split(',')
allowed_origins.extend(config_origins)

# Remover duplicatas e valores vazios
allowed_origins = list(set(filter(None, allowed_origins)))

CORS(app, 
     origins=allowed_origins,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
     supports_credentials=True)
```

### 2. Middleware CORS Personalizado

```python
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    
    # Verificar se a origem está na lista de origens permitidas
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        # Para desenvolvimento local, permitir localhost
        if origin and origin.startswith('http://localhost'):
            response.headers['Access-Control-Allow-Origin'] = origin
    
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response
```

### 3. Endpoint para Requisições OPTIONS (Preflight)

```python
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return '', 200
```

### 4. Configuração Vercel (`vercel.json`)

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "https://gat-fireng-frontend.vercel.app"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization, X-Requested-With"
        },
        {
          "key": "Access-Control-Allow-Credentials",
          "value": "true"
        },
        {
          "key": "Access-Control-Max-Age",
          "value": "86400"
        }
      ]
    }
  ]
}
```

### 5. Configuração de Ambiente (`.env`)

```
# CORS - Incluindo domínio do frontend em produção
CORS_ORIGINS=https://gat-fireng-frontend.vercel.app,http://localhost:3000,http://localhost:5173,http://localhost:5174
```

## 🧪 Testes Realizados

### Teste de Preflight (OPTIONS)
```bash
curl -H "Origin: https://gat-fireng-frontend.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS http://localhost:5001/api/health -v
```

**Resultado**: ✅ Headers CORS corretos retornados

### Teste de Requisição GET
```bash
curl -H "Origin: https://gat-fireng-frontend.vercel.app" \
     http://localhost:5001/api/health -v
```

**Resultado**: ✅ `Access-Control-Allow-Origin: https://gat-fireng-frontend.vercel.app`

## 🔧 Características da Solução

### ✅ Vantagens
- **Específica**: Permite apenas origens autorizadas
- **Flexível**: Suporta desenvolvimento local e produção
- **Robusta**: Múltiplas camadas de proteção CORS
- **Configurável**: Origens podem ser definidas via `.env`

### 🛡️ Segurança
- Não usa `*` (wildcard) para produção
- Validação específica de origens
- Suporte a credenciais quando necessário
- Headers CORS explícitos

### 🔄 Compatibilidade
- **Desenvolvimento**: Suporta localhost em várias portas
- **Produção**: Configurado para Vercel
- **Frontend**: Compatível com `https://gat-fireng-frontend.vercel.app`

## 📝 Próximos Passos

1. **Deploy**: Fazer deploy das alterações no Vercel
2. **Teste**: Verificar se o frontend consegue fazer requisições
3. **Monitoramento**: Acompanhar logs para identificar outros problemas

## 🔗 Links Úteis

- [Documentação CORS do MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Vercel Headers Configuration](https://vercel.com/docs/concepts/projects/project-configuration#headers)
