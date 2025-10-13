from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from datetime import datetime, timedelta, date
from ..models import db, Contract, Equipment, Inspection, Client, Branch, Inventory
from ..decorators import role_required

auto_inspections_bp = Blueprint('auto_inspections', __name__)

@auto_inspections_bp.route('/generate', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def generate_auto_inspections():
    """Gera inspeções automaticamente baseadas em contratos ativos e equipamentos
    ---
    tags:
      - 🤖 GAT - Geração Automática
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            months_ahead:
              type: integer
              example: 3
              description: Quantos meses à frente gerar inspeções
            contract_id:
              type: integer
              example: 1
              description: ID específico do contrato (opcional)
            branch_id:
              type: integer
              example: 1
              description: ID específico da filial (opcional)
    responses:
      200:
        description: Inspeções geradas com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            generated_count:
              type: integer
            inspections:
              type: array
              items:
                type: object
      400:
        description: Erro na requisição
      401:
        description: Token inválido
      403:
        description: Acesso negado
    """
    try:
        data = request.get_json() or {}
        months_ahead = data.get('months_ahead', 3)
        contract_id = data.get('contract_id')
        branch_id = data.get('branch_id')
        
        # Validar parâmetros
        if months_ahead < 1 or months_ahead > 12:
            return jsonify({'error': 'months_ahead deve estar entre 1 e 12'}), 400
        
        generated_inspections = []
        
        # Buscar contratos ativos
        contracts_query = Contract.query.filter_by(status=Contract.STATUS_ACTIVE)
        
        if contract_id:
            contracts_query = contracts_query.filter_by(id=contract_id)
        
        contracts = contracts_query.all()
        
        if not contracts:
            return jsonify({
                'message': 'Nenhum contrato ativo encontrado',
                'generated_count': 0,
                'inspections': []
            }), 200
        
        # Para cada contrato ativo
        for contract in contracts:
            # Buscar filiais da empresa
            branches_query = Branch.query.filter_by(company_id=contract.company_id)
            
            if branch_id:
                branches_query = branches_query.filter_by(id=branch_id)
            
            branches = branches_query.all()
            
            # Para cada filial
            for branch in branches:
                # Buscar inventário da filial
                inventory = Inventory.query.filter_by(branch_id=branch.id).first()
                
                if not inventory:
                    continue
                
                # Buscar equipamentos do inventário
                equipments = Equipment.query.filter_by(inventory_id=inventory.id).all()
                
                # Para cada equipamento
                for equipment in equipments:
                    # Calcular próximas datas de inspeção
                    inspection_dates = calculate_inspection_dates(
                        equipment, months_ahead
                    )
                    
                    # Criar inspeções para cada data
                    for inspection_date in inspection_dates:
                        # Verificar se já existe inspeção para esta data/equipamento
                        existing = Inspection.query.filter_by(
                            equipment_id=equipment.id,
                            scheduled_date=inspection_date,
                            status=Inspection.STATUS_PENDING
                        ).first()
                        
                        if existing:
                            continue
                        
                        # Criar nova inspeção
                        inspection = Inspection(
                            title=f"Inspeção {equipment.name} - {branch.name}",
                            description=f"Inspeção periódica do equipamento {equipment.name} conforme contrato {contract.contract_number}",
                            scheduled_date=inspection_date,
                            status=Inspection.STATUS_PENDING,
                            priority='media',
                            location=equipment.location or branch.address,
                            equipment=equipment.name,
                            client_id=contract.company_id,
                            branch_id=branch.id,
                            equipment_id=equipment.id,
                            contract_id=contract.id,
                            created_by=get_jwt_identity()
                        )
                        
                        db.session.add(inspection)
                        generated_inspections.append(inspection)
        
        # Salvar no banco
        db.session.commit()
        
        # Serializar inspeções geradas
        inspections_data = []
        for inspection in generated_inspections:
            inspections_data.append({
                'id': inspection.id,
                'title': inspection.title,
                'description': inspection.description,
                'scheduled_date': inspection.scheduled_date.isoformat(),
                'status': inspection.status,
                'priority': inspection.priority,
                'location': inspection.location,
                'equipment': inspection.equipment,
                'client_id': inspection.client_id,
                'branch_id': inspection.branch_id,
                'equipment_id': inspection.equipment_id,
                'contract_id': inspection.contract_id,
                'team_id': inspection.team_id
            })
        
        return jsonify({
            'message': f'Inspeções geradas com sucesso',
            'generated_count': len(generated_inspections),
            'inspections': inspections_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao gerar inspeções: {str(e)}'}), 500

def calculate_inspection_dates(equipment, months_ahead):
    """Calcula as datas de inspeção baseadas no tipo de equipamento"""
    dates = []
    today = date.today()
    end_date = today + timedelta(days=months_ahead * 30)
    
    # Definir periodicidade por tipo de equipamento
    inspection_intervals = {
        Equipment.TYPE_EXTINGUISHER: 30,  # Mensal
        Equipment.TYPE_HYDRANT: 90,       # Trimestral
        Equipment.TYPE_SPRINKLER: 180,    # Semestral
        Equipment.TYPE_ALARM: 30,        # Mensal
        Equipment.TYPE_EMERGENCY_LIGHT: 90, # Trimestral
        Equipment.TYPE_FIRE_DOOR: 180,    # Semestral
        Equipment.TYPE_HOSE: 90,          # Trimestral
        Equipment.TYPE_PUMP: 90,          # Trimestral
    }
    
    interval_days = inspection_intervals.get(equipment.type, 90)  # Padrão: trimestral
    
    # Se o equipamento tem data da última inspeção, usar como base
    if equipment.last_inspection_date:
        base_date = equipment.last_inspection_date
    else:
        # Se não tem, usar data de instalação ou hoje
        base_date = equipment.installation_date or today
    
    # Calcular próximas datas
    current_date = base_date
    while current_date <= end_date:
        if current_date >= today:
            dates.append(datetime.combine(current_date, datetime.min.time()))
        current_date += timedelta(days=interval_days)
    
    return dates

@auto_inspections_bp.route('/preview', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def preview_auto_inspections():
    """Preview das inspeções que seriam geradas automaticamente
    ---
    tags:
      - 🤖 GAT - Geração Automática
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            months_ahead:
              type: integer
              example: 3
            contract_id:
              type: integer
              example: 1
            branch_id:
              type: integer
              example: 1
    responses:
      200:
        description: Preview das inspeções
        schema:
          type: object
          properties:
            message:
              type: string
            preview_count:
              type: integer
            preview:
              type: array
              items:
                type: object
    """
    try:
        data = request.get_json() or {}
        months_ahead = data.get('months_ahead', 3)
        contract_id = data.get('contract_id')
        branch_id = data.get('branch_id')
        
        preview_data = []
        
        # Buscar contratos ativos
        contracts_query = Contract.query.filter_by(status=Contract.STATUS_ACTIVE)
        
        if contract_id:
            contracts_query = contracts_query.filter_by(id=contract_id)
        
        contracts = contracts_query.all()
        
        for contract in contracts:
            # Buscar filiais da empresa
            branches_query = Branch.query.filter_by(company_id=contract.company_id)
            
            if branch_id:
                branches_query = branches_query.filter_by(id=branch_id)
            
            branches = branches_query.all()
            
            for branch in branches:
                # Buscar inventário da filial
                inventory = Inventory.query.filter_by(branch_id=branch.id).first()
                
                if not inventory:
                    continue
                
                # Buscar equipamentos do inventário
                equipments = Equipment.query.filter_by(inventory_id=inventory.id).all()
                
                for equipment in equipments:
                    # Calcular próximas datas de inspeção
                    inspection_dates = calculate_inspection_dates(
                        equipment, months_ahead
                    )
                    
                    for inspection_date in inspection_dates:
                        # Verificar se já existe inspeção para esta data/equipamento
                        existing = Inspection.query.filter_by(
                            equipment_id=equipment.id,
                            scheduled_date=inspection_date,
                            status=Inspection.STATUS_PENDING
                        ).first()
                        
                        preview_data.append({
                            'contract_number': contract.contract_number,
                            'company_name': contract.company.name if contract.company else 'N/A',
                            'branch_name': branch.name,
                            'equipment_name': equipment.name,
                            'equipment_type': equipment.type,
                            'scheduled_date': inspection_date.isoformat(),
                            'location': equipment.location or branch.address,
                            'already_exists': existing is not None,
                            'existing_inspection_id': existing.id if existing else None
                        })
        
        return jsonify({
            'message': 'Preview das inspeções que seriam geradas',
            'preview_count': len(preview_data),
            'preview': preview_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar preview: {str(e)}'}), 500

@auto_inspections_bp.route('/stats', methods=['GET'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def get_auto_inspection_stats():
    """Estatísticas para geração automática de inspeções
    ---
    tags:
      - 🤖 GAT - Geração Automática
    security:
      - Bearer: []
    responses:
      200:
        description: Estatísticas das inspeções
        schema:
          type: object
          properties:
            active_contracts:
              type: integer
            total_branches:
              type: integer
            total_equipments:
              type: integer
            pending_inspections:
              type: integer
            contracts_with_equipments:
              type: array
              items:
                type: object
    """
    try:
        # Contratos ativos
        active_contracts = Contract.query.filter_by(status=Contract.STATUS_ACTIVE).count()
        
        # Filiais com equipamentos
        branches_with_equipments = db.session.query(Branch).join(Inventory).join(Equipment).distinct().count()
        
        # Total de equipamentos
        total_equipments = Equipment.query.count()
        
        # Inspeções pendentes
        pending_inspections = Inspection.query.filter_by(status=Inspection.STATUS_PENDING).count()
        
        # Contratos com equipamentos
        contracts_with_equipments = []
        contracts = Contract.query.filter_by(status=Contract.STATUS_ACTIVE).all()
        
        for contract in contracts:
            branches = Branch.query.filter_by(company_id=contract.company_id).all()
            equipments_count = 0
            
            for branch in branches:
                inventory = Inventory.query.filter_by(branch_id=branch.id).first()
                if inventory:
                    equipments_count += Equipment.query.filter_by(inventory_id=inventory.id).count()
            
            if equipments_count > 0:
                contracts_with_equipments.append({
                    'contract_id': contract.id,
                    'contract_number': contract.contract_number,
                    'company_name': contract.company.name if contract.company else 'N/A',
                    'branches_count': len(branches),
                    'equipments_count': equipments_count
                })
        
        return jsonify({
            'active_contracts': active_contracts,
            'total_branches': branches_with_equipments,
            'total_equipments': total_equipments,
            'pending_inspections': pending_inspections,
            'contracts_with_equipments': contracts_with_equipments
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao obter estatísticas: {str(e)}'}), 500
