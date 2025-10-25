#!/usr/bin/env python3
"""
Script para testar endpoints após correções
"""

import requests
import json

# Configuração
BACKEND_URL = "https://gat-fireng-backend.vercel.app/api"
TEST_EMAIL = "admin@fireng.com"
TEST_PASSWORD = "admin123"

def get_auth_token():
    """Obtém token de autenticação"""
    print("Obtendo token de autenticacao...")
    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"Token obtido: {token[:20]}...")
            return token
        else:
            print(f"Erro no login: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None
            
    except Exception as e:
        print(f"Erro ao obter token: {e}")
        return None

def test_endpoint(endpoint, token, method='GET', data=None):
    """Testa um endpoint específico"""
    print(f"\nTestando {method} {endpoint}...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        if method == 'GET':
            response = requests.get(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(f"{BACKEND_URL}{endpoint}", json=data, headers=headers, timeout=10)
        elif method == 'PUT':
            response = requests.put(f"{BACKEND_URL}{endpoint}", json=data, headers=headers, timeout=10)
        elif method == 'DELETE':
            response = requests.delete(f"{BACKEND_URL}{endpoint}", headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Sucesso! Resposta: {json.dumps(data, indent=2)[:200]}...")
                return True
            except:
                print(f"Sucesso! Resposta: {response.text[:200]}...")
                return True
        else:
            print(f"Falhou: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Erro: {error_data}")
            except:
                print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro na requisicao: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("Iniciando testes de endpoints...")
    print("=" * 50)
    
    # Obter token
    token = get_auth_token()
    if not token:
        print("Nao foi possivel obter token. Abortando testes.")
        return
    
    # Lista de endpoints para testar
    endpoints = [
        ("/clients", "GET"),
        ("/users", "GET"),
        ("/inspections", "GET"),
        ("/maintenances", "GET"),
        ("/teams", "GET"),
        ("/technicians", "GET"),
        ("/branches", "GET"),
        ("/contracts", "GET"),
        ("/equipments", "GET"),
        ("/inventories", "GET"),
        ("/standards", "GET")
    ]
    
    results = []
    for endpoint, method in endpoints:
        result = test_endpoint(endpoint, token, method)
        results.append((endpoint, result))
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES:")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for endpoint, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{endpoint}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"TOTAL: {passed + failed} testes")
    print(f"PASSARAM: {passed}")
    print(f"FALHARAM: {failed}")
    
    if failed == 0:
        print("TODOS OS ENDPOINTS ESTAO FUNCIONANDO!")
    else:
        print(f"ALGUNS ENDPOINTS AINDA ESTAO COM PROBLEMAS ({failed} falharam)")
    print("=" * 50)

if __name__ == "__main__":
    main()
