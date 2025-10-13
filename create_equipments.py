#!/usr/bin/env python3
"""
Script para criar equipamentos para os inventários existentes
"""

import requests
import json
from datetime import datetime, timedelta

def create_equipments():
    """Cria equipamentos para os inventários"""
    
    # Headers de autenticação
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDAyMjYwMiwianRpIjoiZjg0NGY0MjItZTNmYi00MjVlLWEyNjktOGI1YjYxMTQyMjJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU4IiwibmJmIjoxNzYwMDIyNjAyLCJjc3JmIjoiMzY3MjRmYTUtYzlhZi00NDQzLWI4YjMtMDFiMzEzNTRmM2Y1IiwiZXhwIjoxNzYwMTA5MDAyfQ.Eet5C3FBi_K0PEgyeBboWzJ0pfquQ0zceaH5W1INqOE',
        'Content-Type': 'application/json'
    }
    
    # Dados dos inventários (ID, Nome da Filial)
    inventories = [
        (2, 'Shopping Paulista - Torre Norte'),
        (3, 'Shopping Paulista - Torre Sul'),
        (4, 'Hospital São Lucas'),
        (5, 'Condomínio Vista Verde'),
        (6, 'Metalúrgica ABC'),
        (7, 'Terra Nova Center'),
        (8, 'Nova Filial Teste')
    ]
    
    # Tipos de equipamentos com dados de exemplo
    equipment_types = [
        {
            'type': 'extintor',
            'equipments': [
                {'name': 'Extintor ABC 6kg', 'capacity': '6kg', 'location': '1º andar - Corredor A'},
                {'name': 'Extintor ABC 4kg', 'capacity': '4kg', 'location': '1º andar - Corredor B'},
                {'name': 'Extintor ABC 6kg', 'capacity': '6kg', 'location': '2º andar - Corredor A'},
                {'name': 'Extintor CO2 5kg', 'capacity': '5kg', 'location': 'Sala de Servidores'},
            ]
        },
        {
            'type': 'hidrante',
            'equipments': [
                {'name': 'Hidrante 40mm', 'capacity': '40mm', 'location': '1º andar - Corredor Principal'},
                {'name': 'Hidrante 25mm', 'capacity': '25mm', 'location': '2º andar - Corredor Principal'},
            ]
        },
        {
            'type': 'sprinkler',
            'equipments': [
                {'name': 'Sprinkler 68°C', 'capacity': '68°C', 'location': '1º andar - Sala 101'},
                {'name': 'Sprinkler 68°C', 'capacity': '68°C', 'location': '1º andar - Sala 102'},
                {'name': 'Sprinkler 68°C', 'capacity': '68°C', 'location': '2º andar - Sala 201'},
            ]
        },
        {
            'type': 'alarme',
            'equipments': [
                {'name': 'Central de Alarme', 'capacity': '24 zonas', 'location': 'Sala de Controle'},
                {'name': 'Detector de Fumaça', 'capacity': 'Óptico', 'location': '1º andar - Corredor A'},
                {'name': 'Detector de Fumaça', 'capacity': 'Óptico', 'location': '2º andar - Corredor A'},
            ]
        },
        {
            'type': 'iluminacao_emergencia',
            'equipments': [
                {'name': 'Luminária de Emergência', 'capacity': 'LED 3W', 'location': '1º andar - Saída de Emergência'},
                {'name': 'Luminária de Emergência', 'capacity': 'LED 3W', 'location': '2º andar - Saída de Emergência'},
                {'name': 'Sinalização de Saída', 'capacity': 'LED', 'location': '1º andar - Porta Principal'},
            ]
        }
    ]
    
    print("Criando equipamentos para os inventarios...")
    print("=" * 60)
    
    total_created = 0
    
    for inventory_id, branch_name in inventories:
        print(f"\nInventario: {branch_name} (ID: {inventory_id})")
        print("-" * 40)
        
        for type_data in equipment_types:
            equipment_type = type_data['type']
            equipments = type_data['equipments']
            
            for i, equipment in enumerate(equipments):
                # Calcular datas
                today = datetime.now()
                installation_date = today - timedelta(days=365 + i*30)  # Instalado há 1 ano + variação
                last_inspection = today - timedelta(days=30 + i*5)  # Última inspeção há 1 mês + variação
                next_inspection = today + timedelta(days=30 + i*10)  # Próxima inspeção em 1 mês + variação
                expiry_date = today + timedelta(days=365 + i*60)  # Vencimento em 1 ano + variação
                
                data = {
                    'name': equipment['name'],
                    'type': equipment_type,
                    'manufacturer': 'Fireng Segurança',
                    'model': f'Model-{equipment_type.upper()}-{i+1:03d}',
                    'serial_number': f'SN-{equipment_type.upper()}-{inventory_id:03d}-{i+1:03d}',
                    'tag_number': f'TAG-{inventory_id:03d}-{i+1:03d}',
                    'manufacturing_date': installation_date.strftime('%Y-%m-%d'),
                    'installation_date': installation_date.strftime('%Y-%m-%d'),
                    'last_inspection_date': last_inspection.strftime('%Y-%m-%d'),
                    'next_inspection_date': next_inspection.strftime('%Y-%m-%d'),
                    'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                    'status': 'ativo',
                    'location': equipment['location'],
                    'capacity': equipment['capacity'],
                    'notes': f'Equipamento {equipment_type} - {branch_name}',
                    'inventory_id': inventory_id
                }
                
                try:
                    response = requests.post('http://localhost:5000/api/equipments', 
                                           headers=headers, json=data)
                    
                    if response.status_code == 201:
                        result = response.json()
                        equipment_id = result['equipment']['id']
                        print(f"  [OK] {equipment['name']} (ID: {equipment_id})")
                        total_created += 1
                    else:
                        print(f"  [ERRO] {equipment['name']}: {response.status_code}")
                        if response.status_code != 409:  # Não mostrar erro de duplicação
                            print(f"         Resposta: {response.text[:100]}...")
                        
                except Exception as e:
                    print(f"  [ERRO] {equipment['name']}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Total de equipamentos criados: {total_created}")
    print("Concluido!")

if __name__ == '__main__':
    create_equipments()
