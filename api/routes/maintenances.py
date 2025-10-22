from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models import db, Maintenance
from ..decorators import role_required, get_current_user

maintenances_bp = Blueprint('maintenances', __name__)

@maintenances_bp.route('', methods=['GET'])
@jwt_required()
def list_maintenances():
    """Lista manutenções com filtros opcionais"""
    try:
        current_user = get_current_user()
    
        # Filtros
        status = request.args.get('status')
        maintenance_type = request.args.get('type')
        technician_id = request.args.get('technician_id')
        client_id = request.args.get('client_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        query = Maintenance.query
        
        # Técnicos só veem suas próprias manutenções
        if current_user.role == 'tecnico':
            query = query.filter_by(technician_id=current_user.id)
        elif technician_id:
            query = query.filter_by(technician_id=technician_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if maintenance_type:
            query = query.filter_by(maintenance_type=maintenance_type)
        
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from)
                query = query.filter(Maintenance.scheduled_date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_from'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to)
                query = query.filter(Maintenance.scheduled_date <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_to'}), 400
    
        maintenances = query.order_by(Maintenance.scheduled_date.desc()).all()
        
        return jsonify({
            'maintenances': [maintenance.to_dict() for maintenance in maintenances],
            'total': len(maintenances)
        }), 200
    except Exception as e:
        print(f"Erro ao listar manutenções: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': str(e)
        }), 500


@maintenances_bp.route('/<int:maintenance_id>', methods=['GET'])
@jwt_required()
def get_maintenance(maintenance_id):
    """Obtém detalhes de uma manutenção específica"""
    current_user = get_current_user()
    maintenance = Maintenance.query.get(maintenance_id)
    
    if not maintenance:
        return jsonify({'error': 'Manutenção não encontrada'}), 404
    
    # Técnicos só podem ver suas próprias manutenções
    if current_user.role == 'tecnico' and maintenance.technician_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    return jsonify(maintenance.to_dict()), 200


@maintenances_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
def create_maintenance():
    """Cria uma nova manutenção"""
    current_user = get_current_user()
    data = request.get_json()
    
    # Validação básica
    required_fields = ['title', 'scheduled_date', 'client_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400
    
    # Validar data
    try:
        scheduled_date = datetime.fromisoformat(data['scheduled_date'])
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400
    
    # Validar tipo de manutenção
    maintenance_type = data.get('maintenance_type', Maintenance.TYPE_PREVENTIVE)
    if maintenance_type not in Maintenance.TYPES:
        return jsonify({'error': f'Tipo inválido. Opções: {", ".join(Maintenance.TYPES)}'}), 400
    
    # Criar nova manutenção
    maintenance = Maintenance(
        title=data['title'],
        description=data.get('description'),
        maintenance_type=maintenance_type,
        scheduled_date=scheduled_date,
        status=data.get('status', Maintenance.STATUS_PENDING),
        priority=data.get('priority', 'media'),
        location=data.get('location'),
        equipment=data.get('equipment'),
        client_id=data['client_id'],
        technician_id=data.get('technician_id'),
        created_by=current_user.id,
        branch_id=data.get('branch_id'),
        equipment_id=data.get('equipment_id'),
        contract_id=data.get('contract_id'),
        team_id=data.get('team_id')
    )
    
    db.session.add(maintenance)
    db.session.commit()
    
    return jsonify({
        'message': 'Manutenção criada com sucesso',
        'maintenance': maintenance.to_dict()
    }), 201


@maintenances_bp.route('/<int:maintenance_id>', methods=['PUT'])
@jwt_required()
def update_maintenance(maintenance_id):
    """Atualiza uma manutenção"""
    current_user = get_current_user()
    maintenance = Maintenance.query.get(maintenance_id)
    
    if not maintenance:
        return jsonify({'error': 'Manutenção não encontrada'}), 404
    
    # Técnicos só podem atualizar suas próprias manutenções
    if current_user.role == 'tecnico' and maintenance.technician_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    # Atualizar campos permitidos
    if 'title' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.title = data['title']
    
    if 'description' in data:
        maintenance.description = data['description']
    
    if 'maintenance_type' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        if data['maintenance_type'] not in Maintenance.TYPES:
            return jsonify({'error': f'Tipo inválido. Opções: {", ".join(Maintenance.TYPES)}'}), 400
        maintenance.maintenance_type = data['maintenance_type']
    
    if 'scheduled_date' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        try:
            maintenance.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
    
    if 'status' in data:
        if data['status'] not in Maintenance.STATUSES:
            return jsonify({'error': f'Status inválido. Opções: {", ".join(Maintenance.STATUSES)}'}), 400
        maintenance.status = data['status']
        
        # Atualizar data de conclusão se status for concluída
        if data['status'] == Maintenance.STATUS_COMPLETED and not maintenance.completed_date:
            maintenance.completed_date = datetime.utcnow()
    
    if 'priority' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.priority = data['priority']
    
    if 'location' in data:
        maintenance.location = data['location']
    
    if 'equipment' in data:
        maintenance.equipment = data['equipment']
    
    if 'technician_id' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.technician_id = data['technician_id']
    
    if 'branch_id' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.branch_id = data['branch_id']
    
    if 'equipment_id' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.equipment_id = data['equipment_id']
    
    if 'contract_id' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.contract_id = data['contract_id']
    
    if 'team_id' in data and current_user.has_role('superadmin', 'admin', 'coord'):
        maintenance.team_id = data['team_id']
    
    if 'work_performed' in data:
        maintenance.work_performed = data['work_performed']
    
    if 'parts_used' in data:
        maintenance.parts_used = data['parts_used']
    
    if 'observations' in data:
        maintenance.observations = data['observations']
    
    if 'photos' in data:
        maintenance.photos = data['photos']
    
    if 'signature' in data:
        maintenance.signature = data['signature']
    
    if 'labor_cost' in data:
        maintenance.labor_cost = data['labor_cost']
    
    if 'parts_cost' in data:
        maintenance.parts_cost = data['parts_cost']
    
    if 'total_cost' in data:
        maintenance.total_cost = data['total_cost']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Manutenção atualizada com sucesso',
        'maintenance': maintenance.to_dict()
    }), 200


@maintenances_bp.route('/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_maintenance(maintenance_id):
    """Cancela uma manutenção"""
    maintenance = Maintenance.query.get(maintenance_id)
    
    if not maintenance:
        return jsonify({'error': 'Manutenção não encontrada'}), 404
    
    maintenance.status = Maintenance.STATUS_CANCELLED
    db.session.commit()
    
    return jsonify({'message': 'Manutenção cancelada com sucesso'}), 200

