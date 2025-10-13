#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Cria uma estrutura completa e realista para testes
"""

from datetime import datetime, timedelta
from app import create_app
from models import (
    db, User, Client, Branch, Contract, Team, Technician,
    Standard, Inventory, Equipment, Inspection, Maintenance
)

def clear_database():
    """Limpa todos os dados do banco (exceto admin)"""
    print("🗑️  Limpando dados antigos...")
    
    # Ordem de exclusão respeitando foreign keys
    Maintenance.query.delete()
    Inspection.query.delete()
    Equipment.query.delete()
    Inventory.query.delete()
    Standard.query.delete()
    Technician.query.delete()
    Contract.query.delete()
    Branch.query.delete()
    Client.query.delete()
    Team.query.delete()
    
    # Manter apenas o admin
    User.query.filter(User.email != 'admin@fireng.com').delete()
    
    db.session.commit()
    print("✅ Dados antigos removidos!\n")


def create_users():
    """Cria usuários de exemplo"""
    print("👥 Criando usuários...")
    
    users = []
    
    # Coordenadores
    coord1 = User(
        email='coord1@fireng.com',
        name='Maria Silva',
        role='coord',
        phone='(11) 98765-4321',
        is_active=True
    )
    coord1.set_password('coord123')
    users.append(coord1)
    
    coord2 = User(
        email='coord2@fireng.com',
        name='João Santos',
        role='coord',
        phone='(11) 98765-4322',
        is_active=True
    )
    coord2.set_password('coord123')
    users.append(coord2)
    
    # Técnicos
    tecnico1 = User(
        email='tecnico1@fireng.com',
        name='Carlos Oliveira',
        role='tecnico',
        phone='(11) 98765-1111',
        is_active=True
    )
    tecnico1.set_password('tecnico123')
    users.append(tecnico1)
    
    tecnico2 = User(
        email='tecnico2@fireng.com',
        name='Ana Paula',
        role='tecnico',
        phone='(11) 98765-2222',
        is_active=True
    )
    tecnico2.set_password('tecnico123')
    users.append(tecnico2)
    
    tecnico3 = User(
        email='tecnico3@fireng.com',
        name='Roberto Lima',
        role='tecnico',
        phone='(11) 98765-3333',
        is_active=True
    )
    tecnico3.set_password('tecnico123')
    users.append(tecnico3)
    
    tecnico4 = User(
        email='tecnico4@fireng.com',
        name='Fernanda Costa',
        role='tecnico',
        phone='(11) 98765-4444',
        is_active=True
    )
    tecnico4.set_password('tecnico123')
    users.append(tecnico4)
    
    # Cliente
    cliente1 = User(
        email='cliente1@empresa.com',
        name='Pedro Martins',
        role='cliente',
        phone='(11) 98765-5555',
        is_active=True
    )
    cliente1.set_password('cliente123')
    users.append(cliente1)
    
    for user in users:
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ {len(users)} usuários criados!\n")
    
    return users


def create_teams(users):
    """Cria equipes de técnicos"""
    print("👥 Criando equipes...")
    
    teams = []
    
    team1 = Team(
        name='Equipe Alpha',
        description='Especializada em manutenção preventiva e inspeções de rotina',
        is_active=True
    )
    teams.append(team1)
    
    team2 = Team(
        name='Equipe Beta',
        description='Especializada em manutenções corretivas e emergenciais',
        is_active=True
    )
    teams.append(team2)
    
    team3 = Team(
        name='Equipe Gamma',
        description='Especializada em instalação de novos equipamentos',
        is_active=True
    )
    teams.append(team3)
    
    for team in teams:
        db.session.add(team)
    
    db.session.commit()
    print(f"✅ {len(teams)} equipes criadas!\n")
    
    return teams


def create_technicians(users, teams):
    """Cria perfis de técnicos"""
    print("🔧 Criando perfis de técnicos...")
    
    technicians = []
    
    # Técnicos da equipe Alpha
    tech1 = Technician(
        user_id=users[2].id,  # Carlos Oliveira
        registration_number='TEC-001',
        specializations='["Extintores", "Hidrantes", "Mangueiras"]',
        certifications='[{"name": "NR 23", "date": "2023-01-15", "expiry": "2026-01-15"}]',
        experience_years=5,
        team_id=teams[0].id
    )
    technicians.append(tech1)
    
    tech2 = Technician(
        user_id=users[3].id,  # Ana Paula
        registration_number='TEC-002',
        specializations='["Sistemas de Alarme", "Detecção de Fumaça"]',
        certifications='[{"name": "NR 10", "date": "2023-03-20", "expiry": "2025-03-20"}]',
        experience_years=3,
        team_id=teams[0].id
    )
    technicians.append(tech2)
    
    # Técnicos da equipe Beta
    tech3 = Technician(
        user_id=users[4].id,  # Roberto Lima
        registration_number='TEC-003',
        specializations='["Sprinklers", "Bombas", "Manutenção Corretiva"]',
        certifications='[{"name": "NR 23", "date": "2022-06-10", "expiry": "2025-06-10"}, {"name": "NR 10", "date": "2022-08-15", "expiry": "2024-08-15"}]',
        experience_years=7,
        team_id=teams[1].id
    )
    technicians.append(tech3)
    
    # Técnico da equipe Gamma
    tech4 = Technician(
        user_id=users[5].id,  # Fernanda Costa
        registration_number='TEC-004',
        specializations='["Instalação", "Projetos", "Laudos Técnicos"]',
        certifications='[{"name": "Eng. Segurança do Trabalho", "date": "2021-01-10", "expiry": null}]',
        experience_years=4,
        team_id=teams[2].id
    )
    technicians.append(tech4)
    
    for tech in technicians:
        db.session.add(tech)
    
    db.session.commit()
    print(f"✅ {len(technicians)} técnicos criados!\n")
    
    return technicians


def create_clients():
    """Cria empresas clientes"""
    print("🏢 Criando empresas clientes...")
    
    clients = []
    
    client1 = Client(
        name='Shopping Center Paulista',
        cpf_cnpj='12.345.678/0001-90',
        email='contato@shoppingpaulista.com.br',
        phone='(11) 3000-1000',
        address='Av. Paulista, 1000',
        city='São Paulo',
        state='SP',
        zip_code='01310-100',
        notes='Contato: Ricardo Almeida',
        is_active=True
    )
    clients.append(client1)
    
    client2 = Client(
        name='Hospital São Lucas',
        cpf_cnpj='23.456.789/0001-01',
        email='administrativo@saolucas.com.br',
        phone='(11) 3000-2000',
        address='Rua da Consolação, 500',
        city='São Paulo',
        state='SP',
        zip_code='01301-000',
        notes='Contato: Dra. Juliana Mendes',
        is_active=True
    )
    clients.append(client2)
    
    client3 = Client(
        name='Condomínio Residencial Vista Verde',
        cpf_cnpj='34.567.890/0001-12',
        email='sindico@vistaverde.com.br',
        phone='(11) 3000-3000',
        address='Rua das Flores, 200',
        city='São Paulo',
        state='SP',
        zip_code='04567-000',
        notes='Contato: Marcos Ferreira (Síndico)',
        is_active=True
    )
    clients.append(client3)
    
    client4 = Client(
        name='Indústria Metalúrgica ABC',
        cpf_cnpj='45.678.901/0001-23',
        email='seguranca@metalurgicaabc.com.br',
        phone='(11) 4000-1000',
        address='Av. Industrial, 1500',
        city='São Bernardo do Campo',
        state='SP',
        zip_code='09750-000',
        notes='Contato: Eng. Paulo Rodrigues',
        is_active=True
    )
    clients.append(client4)
    
    for client in clients:
        db.session.add(client)
    
    db.session.commit()
    print(f"✅ {len(clients)} empresas criadas!\n")
    
    return clients


def create_branches(clients):
    """Cria filiais das empresas"""
    print("🏢 Criando filiais...")
    
    branches = []
    
    # Filiais do Shopping
    branch1 = Branch(
        name='Shopping Paulista - Torre Norte',
        company_id=clients[0].id,
        address='Av. Paulista, 1000 - Torre Norte',
        city='São Paulo',
        state='SP',
        zip_code='01310-100',
        phone='(11) 3000-1001',
        email='torre.norte@shoppingpaulista.com.br',
        is_active=True
    )
    branches.append(branch1)
    
    branch2 = Branch(
        name='Shopping Paulista - Torre Sul',
        company_id=clients[0].id,
        address='Av. Paulista, 1000 - Torre Sul',
        city='São Paulo',
        state='SP',
        zip_code='01310-100',
        phone='(11) 3000-1002',
        email='torre.sul@shoppingpaulista.com.br',
        is_active=True
    )
    branches.append(branch2)
    
    # Filiais do Hospital
    branch3 = Branch(
        name='Hospital São Lucas - Unidade Principal',
        company_id=clients[1].id,
        address='Rua da Consolação, 500',
        city='São Paulo',
        state='SP',
        zip_code='01301-000',
        phone='(11) 3000-2001',
        email='principal@saolucas.com.br',
        is_active=True
    )
    branches.append(branch3)
    
    # Filial do Condomínio
    branch4 = Branch(
        name='Condomínio Vista Verde - Bloco A',
        company_id=clients[2].id,
        address='Rua das Flores, 200 - Bloco A',
        city='São Paulo',
        state='SP',
        zip_code='04567-000',
        phone='(11) 3000-3001',
        email='blocoa@vistaverde.com.br',
        is_active=True
    )
    branches.append(branch4)
    
    # Filial da Indústria
    branch5 = Branch(
        name='Metalúrgica ABC - Planta 1',
        company_id=clients[3].id,
        address='Av. Industrial, 1500 - Galpão 1',
        city='São Bernardo do Campo',
        state='SP',
        zip_code='09750-000',
        phone='(11) 4000-1001',
        email='planta1@metalurgicaabc.com.br',
        is_active=True
    )
    branches.append(branch5)
    
    for branch in branches:
        db.session.add(branch)
    
    db.session.commit()
    print(f"✅ {len(branches)} filiais criadas!\n")
    
    return branches


def create_contracts(clients, branches, teams):
    """Cria contratos de serviços"""
    print("📄 Criando contratos...")
    
    contracts = []
    
    from datetime import date
    
    contract1 = Contract(
        contract_number='CTR-2025-001',
        description='Manutenção preventiva mensal de todos os equipamentos de combate a incêndio',
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        status='ativo',
        value=48000.00,
        company_id=clients[0].id,
        team_id=teams[0].id
    )
    contracts.append(contract1)
    
    contract2 = Contract(
        contract_number='CTR-2025-002',
        description='Manutenção preventiva e corretiva - Hospital',
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        status='ativo',
        value=72000.00,
        company_id=clients[1].id,
        team_id=teams[0].id
    )
    contracts.append(contract2)
    
    contract3 = Contract(
        contract_number='CTR-2025-003',
        description='Manutenção trimestral - Condomínio',
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        status='ativo',
        value=24000.00,
        company_id=clients[2].id,
        team_id=teams[1].id
    )
    contracts.append(contract3)
    
    contract4 = Contract(
        contract_number='CTR-2024-099',
        description='Contrato anterior - Finalizado',
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        status='expirado',
        value=36000.00,
        company_id=clients[3].id,
        team_id=teams[1].id
    )
    contracts.append(contract4)
    
    contract5 = Contract(
        contract_number='CTR-2025-004',
        description='Novo contrato - Indústria',
        start_date=date(2025, 2, 1),
        end_date=date(2026, 1, 31),
        status='ativo',
        value=96000.00,
        company_id=clients[3].id,
        team_id=teams[2].id
    )
    contracts.append(contract5)
    
    for contract in contracts:
        db.session.add(contract)
    
    db.session.commit()
    print(f"✅ {len(contracts)} contratos criados!\n")
    
    return contracts


def create_standards():
    """Cria normas técnicas"""
    print("📋 Criando normas técnicas...")
    
    standards = []
    
    from datetime import date
    
    standard1 = Standard(
        code='NBR 12962',
        name='Extintores de incêndio',
        description='Inspeção, manutenção e recarga em extintores de incêndio',
        type='NBR',
        version='2016',
        publication_date=date(2016, 4, 1)
    )
    standards.append(standard1)
    
    standard2 = Standard(
        code='NBR 13714',
        name='Sistema de hidrantes e mangotinhos',
        description='Sistema de hidrantes e de mangotinhos para combate a incêndio',
        type='NBR',
        version='2000',
        publication_date=date(2000, 1, 1)
    )
    standards.append(standard2)
    
    standard3 = Standard(
        code='NBR 17240',
        name='Sistema de detecção e alarme',
        description='Sistemas de detecção e alarme de incêndio',
        type='NBR',
        version='2010',
        publication_date=date(2010, 9, 1)
    )
    standards.append(standard3)
    
    standard4 = Standard(
        code='NBR 10897',
        name='Sistema de sprinklers',
        description='Sistemas de proteção contra incêndio por chuveiros automáticos',
        type='NBR',
        version='2020',
        publication_date=date(2020, 3, 1)
    )
    standards.append(standard4)
    
    standard5 = Standard(
        code='NR 23',
        name='Proteção contra incêndios',
        description='Norma Regulamentadora sobre proteção contra incêndios',
        type='NR',
        version='2011',
        publication_date=date(2011, 12, 8)
    )
    standards.append(standard5)
    
    standard6 = Standard(
        code='IT 22',
        name='Sistema de hidrantes',
        description='Instrução Técnica do Corpo de Bombeiros - Sistema de hidrantes',
        type='IT',
        version='2019',
        publication_date=date(2019, 1, 1)
    )
    standards.append(standard6)
    
    for standard in standards:
        db.session.add(standard)
    
    db.session.commit()
    print(f"✅ {len(standards)} normas criadas!\n")
    
    return standards


def create_inventories_and_equipments(branches, standards):
    """Cria inventários e equipamentos"""
    print("📦 Criando inventários e equipamentos...")
    
    inventories = []
    equipments = []
    
    from datetime import date
    
    # Inventário Shopping Torre Norte
    inv1 = Inventory(
        branch_id=branches[0].id,
        total_equipments=3,
        last_audit_date=date(2024, 12, 1),
        next_audit_date=date(2025, 12, 1),
        status='atualizado',
        extinguishers_count=2,
        hydrants_count=1
    )
    inventories.append(inv1)
    db.session.add(inv1)
    db.session.flush()
    
    # Equipamentos Torre Norte
    equip1 = Equipment(
        name='Extintor PQS 6kg',
        serial_number='EXT-TN-001',
        model='ABC-6',
        manufacturer='Extinbras',
        installation_date=datetime(2023, 1, 15),
        last_maintenance_date=datetime(2024, 12, 10),
        next_maintenance_date=datetime(2025, 12, 10),
        location_description='Corredor principal - 1º andar - próximo ao elevador',
        inventory_id=inv1.id,
        is_active=True
    )
    equip1.standards.append(standards[0])
    equipments.append(equip1)
    
    equip2 = Equipment(
        name='Extintor PQS 6kg',
        serial_number='EXT-TN-002',
        model='ABC-6',
        manufacturer='Extinbras',
        installation_date=datetime(2023, 1, 15),
        last_maintenance_date=datetime(2024, 12, 10),
        next_maintenance_date=datetime(2025, 12, 10),
        location_description='Corredor principal - 2º andar - próximo à escada',
        inventory_id=inv1.id,
        is_active=True
    )
    equip2.standards.append(standards[0])
    equipments.append(equip2)
    
    equip3 = Equipment(
        name='Hidrante 30m',
        serial_number='HID-TN-001',
        model='HID-30',
        manufacturer='Hydro Systems',
        installation_date=datetime(2023, 1, 20),
        last_maintenance_date=datetime(2024, 11, 5),
        next_maintenance_date=datetime(2025, 11, 5),
        location_description='Hall de entrada - 1º andar',
        inventory_id=inv1.id,
        is_active=True
    )
    equip3.standards.append(standards[1])
    equip3.standards.append(standards[5])
    equipments.append(equip3)
    
    # Inventário Hospital
    inv2 = Inventory(
        branch_id=branches[2].id,
        total_equipments=3,
        last_audit_date=date(2024, 11, 15),
        next_audit_date=date(2025, 11, 15),
        status='atualizado',
        extinguishers_count=1,
        sprinklers_count=1,
        alarms_count=1
    )
    inventories.append(inv2)
    db.session.add(inv2)
    db.session.flush()
    
    # Equipamentos Hospital
    equip4 = Equipment(
        name='Extintor CO2 6kg',
        serial_number='EXT-HSP-001',
        model='CO2-6',
        manufacturer='Extinbras',
        installation_date=datetime(2023, 3, 10),
        last_maintenance_date=datetime(2024, 12, 15),
        next_maintenance_date=datetime(2025, 12, 15),
        location_description='Centro cirúrgico - Corredor A',
        inventory_id=inv2.id,
        is_active=True
    )
    equip4.standards.append(standards[0])
    equipments.append(equip4)
    
    equip5 = Equipment(
        name='Sistema de Sprinklers',
        serial_number='SPK-HSP-001',
        model='SPK-AUTO',
        manufacturer='Fire Protection Inc',
        installation_date=datetime(2023, 3, 15),
        last_maintenance_date=datetime(2024, 10, 20),
        next_maintenance_date=datetime(2025, 10, 20),
        location_description='Enfermarias - Ala Sul',
        inventory_id=inv2.id,
        is_active=True
    )
    equip5.standards.append(standards[3])
    equipments.append(equip5)
    
    equip6 = Equipment(
        name='Central de Alarme',
        serial_number='ALM-HSP-001',
        model='ALARM-PRO',
        manufacturer='Safety Systems',
        installation_date=datetime(2023, 3, 20),
        last_maintenance_date=datetime(2024, 12, 1),
        next_maintenance_date=datetime(2025, 6, 1),
        location_description='Central de segurança - Térreo',
        inventory_id=inv2.id,
        is_active=True
    )
    equip6.standards.append(standards[2])
    equipments.append(equip6)
    
    # Inventário Condomínio
    inv3 = Inventory(
        branch_id=branches[3].id,
        total_equipments=1,
        last_audit_date=date(2024, 10, 20),
        next_audit_date=date(2025, 10, 20),
        status='atualizado',
        extinguishers_count=1
    )
    inventories.append(inv3)
    db.session.add(inv3)
    db.session.flush()
    
    # Equipamentos Condomínio
    equip7 = Equipment(
        name='Extintor PQS 4kg',
        serial_number='EXT-COND-001',
        model='ABC-4',
        manufacturer='Extinbras',
        installation_date=datetime(2023, 5, 10),
        last_maintenance_date=datetime(2024, 11, 20),
        next_maintenance_date=datetime(2025, 11, 20),
        location_description='Hall do prédio - Térreo',
        inventory_id=inv3.id,
        is_active=True
    )
    equip7.standards.append(standards[0])
    equipments.append(equip7)
    
    # Inventário Indústria
    inv4 = Inventory(
        branch_id=branches[4].id,
        total_equipments=1,
        last_audit_date=date(2024, 12, 5),
        next_audit_date=date(2025, 12, 5),
        status='atualizado',
        extinguishers_count=1
    )
    inventories.append(inv4)
    db.session.add(inv4)
    db.session.flush()
    
    # Equipamentos Indústria
    equip8 = Equipment(
        name='Extintor PQS 12kg',
        serial_number='EXT-IND-001',
        model='ABC-12',
        manufacturer='Industrial Fire',
        installation_date=datetime(2024, 2, 1),
        last_maintenance_date=datetime(2024, 12, 5),
        next_maintenance_date=datetime(2025, 12, 5),
        location_description='Galpão 1 - Setor de solda',
        inventory_id=inv4.id,
        is_active=True
    )
    equip8.standards.append(standards[0])
    equip8.standards.append(standards[4])
    equipments.append(equip8)
    
    for equip in equipments:
        db.session.add(equip)
    
    db.session.commit()
    print(f"✅ {len(inventories)} inventários e {len(equipments)} equipamentos criados!\n")
    
    return inventories, equipments


def create_inspections(clients, branches, equipments, contracts, teams, technicians, users):
    """Cria inspeções de exemplo"""
    print("📋 Criando inspeções...")
    
    inspections = []
    
    # Inspeção concluída
    insp1 = Inspection(
        title='Inspeção Mensal - Janeiro 2025',
        description='Inspeção de rotina dos equipamentos da Torre Norte',
        scheduled_date=datetime(2025, 1, 15, 9, 0),
        completed_date=datetime(2025, 1, 15, 11, 30),
        status='concluida',
        priority='media',
        location='Shopping Paulista - Torre Norte',
        equipment='Extintores e Hidrantes',
        client_id=clients[0].id,
        branch_id=branches[0].id,
        equipment_id=equipments[0].id,
        contract_id=contracts[0].id,
        team_id=teams[0].id,
        technician_id=technicians[0].user_id,
        created_by=users[0].id,
        findings='Todos os equipamentos em conformidade. Pressão dos extintores OK.',
        recommendations='Manter cronograma de manutenção preventiva.',
        photos='["foto1.jpg", "foto2.jpg"]'
    )
    inspections.append(insp1)
    
    # Inspeção em andamento
    insp2 = Inspection(
        title='Inspeção Trimestral - Hospital',
        description='Inspeção completa do sistema de combate a incêndio',
        scheduled_date=datetime(2025, 1, 20, 8, 0),
        status='em_andamento',
        priority='alta',
        location='Hospital São Lucas',
        equipment='Sprinklers, Alarmes e Extintores',
        client_id=clients[1].id,
        branch_id=branches[2].id,
        equipment_id=equipments[4].id,
        contract_id=contracts[1].id,
        team_id=teams[0].id,
        technician_id=technicians[1].user_id,
        created_by=users[0].id,
        findings='Inspeção em andamento...'
    )
    inspections.append(insp2)
    
    # Inspeção pendente
    insp3 = Inspection(
        title='Inspeção Mensal - Fevereiro 2025',
        description='Inspeção de rotina dos equipamentos',
        scheduled_date=datetime(2025, 2, 15, 9, 0),
        status='pendente',
        priority='media',
        location='Shopping Paulista - Torre Sul',
        equipment='Extintores',
        client_id=clients[0].id,
        branch_id=branches[1].id,
        contract_id=contracts[0].id,
        team_id=teams[0].id,
        technician_id=technicians[0].user_id,
        created_by=users[0].id
    )
    inspections.append(insp3)
    
    # Inspeção pendente - Condomínio
    insp4 = Inspection(
        title='Inspeção Semestral - Condomínio',
        description='Inspeção semestral conforme contrato',
        scheduled_date=datetime(2025, 2, 10, 14, 0),
        status='pendente',
        priority='baixa',
        location='Condomínio Vista Verde',
        equipment='Extintores',
        client_id=clients[2].id,
        branch_id=branches[3].id,
        equipment_id=equipments[6].id,
        contract_id=contracts[2].id,
        team_id=teams[1].id,
        technician_id=technicians[2].user_id,
        created_by=users[1].id
    )
    inspections.append(insp4)
    
    for insp in inspections:
        db.session.add(insp)
    
    db.session.commit()
    print(f"✅ {len(inspections)} inspeções criadas!\n")
    
    return inspections


def create_maintenances(clients, branches, equipments, contracts, teams, technicians, users):
    """Cria manutenções de exemplo"""
    print("🔧 Criando manutenções...")
    
    maintenances = []
    
    # Manutenção preventiva concluída
    maint1 = Maintenance(
        title='Recarga de Extintor PQS 6kg',
        description='Recarga anual do extintor conforme NBR 12962',
        maintenance_type='preventiva',
        scheduled_date=datetime(2024, 12, 10, 10, 0),
        completed_date=datetime(2024, 12, 10, 11, 0),
        status='concluida',
        priority='media',
        location='Shopping Paulista - Torre Norte',
        equipment='Extintor PQS 6kg - EXT-TN-001',
        client_id=clients[0].id,
        branch_id=branches[0].id,
        equipment_id=equipments[0].id,
        contract_id=contracts[0].id,
        team_id=teams[0].id,
        technician_id=technicians[0].user_id,
        created_by=users[0].id,
        work_performed='Recarga completa do extintor com pó químico seco ABC. Teste de pressão realizado.',
        parts_used='6kg de pó químico ABC, lacre de segurança, etiqueta de identificação',
        observations='Equipamento em perfeitas condições.',
        labor_cost=80.00,
        parts_cost=45.00,
        total_cost=125.00
    )
    maintenances.append(maint1)
    
    # Manutenção corretiva concluída
    maint2 = Maintenance(
        title='Reparo de Hidrante',
        description='Substituição de mangueira danificada',
        maintenance_type='corretiva',
        scheduled_date=datetime(2024, 11, 5, 14, 0),
        completed_date=datetime(2024, 11, 5, 16, 30),
        status='concluida',
        priority='alta',
        location='Shopping Paulista - Torre Norte',
        equipment='Hidrante 30m - HID-TN-001',
        client_id=clients[0].id,
        branch_id=branches[0].id,
        equipment_id=equipments[2].id,
        contract_id=contracts[0].id,
        team_id=teams[1].id,
        technician_id=technicians[2].user_id,
        created_by=users[0].id,
        work_performed='Substituição de mangueira de 30m danificada. Teste de vazão realizado.',
        parts_used='Mangueira tipo 2 de 30m, abraçadeiras, esguicho regulável',
        observations='Mangueira anterior apresentava furos. Teste de pressão OK.',
        labor_cost=200.00,
        parts_cost=850.00,
        total_cost=1050.00
    )
    maintenances.append(maint2)
    
    # Manutenção preventiva agendada
    maint3 = Maintenance(
        title='Manutenção Sistema de Sprinklers',
        description='Manutenção semestral do sistema de sprinklers',
        maintenance_type='preventiva',
        scheduled_date=datetime(2025, 10, 20, 8, 0),
        status='agendada',
        priority='alta',
        location='Hospital São Lucas',
        equipment='Sistema de Sprinklers - SPK-HSP-001',
        client_id=clients[1].id,
        branch_id=branches[2].id,
        equipment_id=equipments[4].id,
        contract_id=contracts[1].id,
        team_id=teams[0].id,
        technician_id=technicians[1].user_id,
        created_by=users[0].id
    )
    maintenances.append(maint3)
    
    # Manutenção emergencial em andamento
    maint4 = Maintenance(
        title='Emergência - Central de Alarme',
        description='Central de alarme apresentando falha',
        maintenance_type='emergencial',
        scheduled_date=datetime.now(),
        status='em_andamento',
        priority='urgente',
        location='Hospital São Lucas',
        equipment='Central de Alarme - ALM-HSP-001',
        client_id=clients[1].id,
        branch_id=branches[2].id,
        equipment_id=equipments[5].id,
        contract_id=contracts[1].id,
        team_id=teams[1].id,
        technician_id=technicians[2].user_id,
        created_by=users[1].id,
        work_performed='Diagnóstico em andamento. Identificada falha no módulo de comunicação.',
        observations='Acionamento emergencial. Cliente aguardando resolução.'
    )
    maintenances.append(maint4)
    
    # Instalação agendada
    maint5 = Maintenance(
        title='Instalação de Novos Extintores',
        description='Instalação de 5 novos extintores conforme projeto',
        maintenance_type='instalacao',
        scheduled_date=datetime(2025, 2, 1, 9, 0),
        status='agendada',
        priority='media',
        location='Metalúrgica ABC - Planta 1',
        equipment='5x Extintor PQS 12kg',
        client_id=clients[3].id,
        branch_id=branches[4].id,
        contract_id=contracts[4].id,
        team_id=teams[2].id,
        technician_id=technicians[3].user_id,
        created_by=users[1].id
    )
    maintenances.append(maint5)
    
    for maint in maintenances:
        db.session.add(maint)
    
    db.session.commit()
    print(f"✅ {len(maintenances)} manutenções criadas!\n")
    
    return maintenances


def seed_database():
    """Executa todo o processo de seed"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("🌱 INICIANDO SEED DO BANCO DE DADOS")
        print("="*80 + "\n")
        
        # Limpar dados antigos
        clear_database()
        
        # Criar dados em ordem
        users = create_users()
        teams = create_teams(users)
        technicians = create_technicians(users, teams)
        clients = create_clients()
        branches = create_branches(clients)
        contracts = create_contracts(clients, branches, teams)
        standards = create_standards()
        # inventories, equipments = create_inventories_and_equipments(branches, standards)
        # inspections = create_inspections(clients, branches, equipments, contracts, teams, technicians, users)
        # maintenances = create_maintenances(clients, branches, equipments, contracts, teams, technicians, users)
        inventories = []
        equipments = []
        inspections = []
        maintenances = []
        
        print("\n" + "="*80)
        print("✨ SEED CONCLUÍDO COM SUCESSO!")
        print("="*80 + "\n")
        
        print("📊 RESUMO:")
        print(f"  • {len(users)} usuários")
        print(f"  • {len(teams)} equipes")
        print(f"  • {len(technicians)} técnicos")
        print(f"  • {len(clients)} empresas")
        print(f"  • {len(branches)} filiais")
        print(f"  • {len(contracts)} contratos")
        print(f"  • {len(standards)} normas")
        print(f"  • {len(inventories)} inventários")
        print(f"  • {len(equipments)} equipamentos")
        print(f"  • {len(inspections)} inspeções")
        print(f"  • {len(maintenances)} manutenções")
        
        print("\n" + "="*80)
        print("🔐 CREDENCIAIS DE ACESSO:")
        print("="*80)
        print("\n📧 Admin:")
        print("   Email: admin@fireng.com")
        print("   Senha: admin123")
        print("\n📧 Coordenadores:")
        print("   Email: coord1@fireng.com / coord2@fireng.com")
        print("   Senha: coord123")
        print("\n📧 Técnicos:")
        print("   Email: tecnico1@fireng.com até tecnico4@fireng.com")
        print("   Senha: tecnico123")
        print("\n📧 Cliente:")
        print("   Email: cliente1@empresa.com")
        print("   Senha: cliente123")
        
        print("\n" + "="*80)
        print("🚀 Acesse: http://localhost:5000/api/docs")
        print("="*80 + "\n")


if __name__ == '__main__':
    seed_database()
