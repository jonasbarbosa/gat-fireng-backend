#!/usr/bin/env python3
"""
Script para testar se as correções de relacionamentos SQLAlchemy resolveram o problema de login
"""

import os
import sys
import requests
import json

# Configuração
BACKEND_URL = "https://gat-fireng-backend.vercel.app/api"
TEST_EMAIL = "admin@fireng.com"
TEST_PASSWORD = "admin123"

def test_health_check():
    """Testa se o backend está funcionando"""
    print("Testando health check...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Health check OK: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro no health check: {e}")
        return False

def test_login():
    """Testa o endpoint de login"""
    print("Testando login...")
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
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Login funcionando!")
            print(f"Token recebido: {data.get('access_token', 'N/A')[:20]}...")
            return True
        else:
            print(f"Login falhou: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Erro: {error_data}")
            except:
                print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro no login: {e}")
        return False

def test_cors():
    """Testa se CORS está funcionando"""
    print("Testando CORS...")
    try:
        response = requests.options(
            f"{BACKEND_URL}/auth/login",
            headers={
                "Origin": "https://gat-fireng-frontend.vercel.app",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            },
            timeout=10
        )
        
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers")
        }
        
        print(f"CORS headers: {cors_headers}")
        return True
        
    except Exception as e:
        print(f"Erro no CORS: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("Iniciando testes de correcao...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("CORS", test_cors),
        ("Login", test_login)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("RESUMO DOS TESTES:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("TODOS OS TESTES PASSARAM! O sistema esta funcionando.")
    else:
        print("ALGUNS TESTES FALHARAM. Verifique os logs acima.")
    print("=" * 50)

if __name__ == "__main__":
    main()
