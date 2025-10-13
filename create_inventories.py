#!/usr/bin/env python3
"""
Script para criar inventários para todas as filiais existentes
"""

import requests
import json

def create_inventories():
    """Cria inventários para todas as filiais"""
    
    # Headers de autenticação
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDAyMjYwMiwianRpIjoiZjg0NGY0MjItZTNmYi00MjVlLWEyNjktOGI1YjYxMTQyMjJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU4IiwibmJmIjoxNzYwMDIyNjAyLCJjc3JmIjoiMzY3MjRmYTUtYzlhZi00NDQzLWI4YjMtMDFiMzEzNTRmM2Y1IiwiZXhwIjoxNzYwMTA5MDAyfQ.Eet5C3FBi_K0PEgyeBboWzJ0pfquQ0zceaH5W1INqOE',
        'Content-Type': 'application/json'
    }
    
    # Dados das filiais (ID, Nome)
    branches = [
        (22, 'Torre Sul'),
        (23, 'Hospital São Lucas'),
        (24, 'Condomínio Vista Verde'),
        (25, 'Metalúrgica ABC'),
        (26, 'Terra Nova Center'),
        (28, 'Nova Filial Teste')
    ]
    
    print("Criando inventários para todas as filiais...")
    print("=" * 50)
    
    for branch_id, name in branches:
        data = {
            'branch_id': branch_id,
            'status': 'atualizado',
            'notes': f'Inventário da {name}'
        }
        
        try:
            response = requests.post('http://localhost:5000/api/inventories', 
                                   headers=headers, json=data)
            
            if response.status_code == 201:
                result = response.json()
                inventory_id = result['inventory']['id']
                print(f"[OK] Inventario criado para {name} (ID: {inventory_id})")
            elif response.status_code == 409:
                print(f"[INFO] Inventario ja existe para {name}")
            else:
                print(f"[ERRO] Erro ao criar inventario para {name}: {response.status_code}")
                print(f"   Resposta: {response.text[:100]}...")
                
        except Exception as e:
            print(f"[ERRO] Erro de conexao para {name}: {e}")
    
    print("=" * 50)
    print("Concluído!")

if __name__ == '__main__':
    create_inventories()
