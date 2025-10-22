from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from ..models import db, Inspection, Client, Team, User, Branch, Equipment, Contract
from ..decorators import role_required, get_current_user
from flasgger import swag_from

inspections_bp = Blueprint('inspections', __name__)

@inspections_bp.route('', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['📋 DAT - Inspeções'],
    'summary': 'Lista inspeções com filtros',
    'description': 'Retorna lista de inspeções com filtros opcionais',
    'parameters': [
        {
            'in': 'query',
            'name': 'status',
            'type': 'string',
            'description': 'Filtrar por status'
        },
        {
            'in': 'query',
            'name': 'technician_id',
            'type': 'integer',
            'description': 'Filtrar por técnico'
        },
        {
            'in': 'query',
            'name': 'client_id',
            'type': 'integer',
            'description': 'Filtrar por cliente'
        },
        {
            'in': 'query',
            'name': 'team_id',
            'type': 'integer',
            'description': 'Filtrar por equipe'
        },
        {
            'in': 'query',
            'name': 'date_from',
            'type': 'string',
            'format': 'date',
            'description': 'Data inicial (YYYY-MM-DD)'
        },
        {
            'in': 'query',
            'name': 'date_to',
            'type': 'string',
            'format': 'date',
            'description': 'Data final (YYYY-MM-DD)'
        },
        {
            'in': 'query',
            'name': 'search_id',
            'type': 'integer',
            'description': 'Buscar por ID específico da inspeção'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de inspeções',
            'schema': {
                'type': 'object',
                'properties': {
                    'inspections': {
                        'type': 'array',
                        'items': {'type': 'object'}
                    },
                    'total': {'type': 'integer'}
                }
            }
        }
    },
    'security': [{'Bearer': []}]
})
def list_inspections():
    """Lista inspeções com filtros opcionais"""
    try:
        current_user = get_current_user()
        
        # Filtros
        status = request.args.get('status')
        technician_id = request.args.get('technician_id')
        client_id = request.args.get('client_id')
        team_id = request.args.get('team_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        search_id = request.args.get('search_id')
        
        query = Inspection.query
        
        # Técnicos só veem suas próprias inspeções
        if current_user.role == 'tecnico':
            query = query.filter_by(technician_id=current_user.id)
        elif technician_id:
            query = query.filter_by(technician_id=technician_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        if team_id:
            query = query.filter_by(team_id=team_id)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from)
                query = query.filter(Inspection.scheduled_date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_from'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to)
                query = query.filter(Inspection.scheduled_date <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Formato de data inválido para date_to'}), 400
        
        # Filtro por ID
        if search_id:
            try:
                search_id_int = int(search_id)
                query = query.filter(Inspection.id == search_id_int)
            except ValueError:
                return jsonify({'error': 'ID deve ser um número inteiro'}), 400
        
        inspections = query.order_by(Inspection.scheduled_date.desc()).all()
        
        return jsonify({
            'inspections': [inspection.to_dict() for inspection in inspections],
            'total': len(inspections)
        }), 200
    except Exception as e:
        print(f"Erro ao listar inspeções: {str(e)}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'message': str(e)
        }), 500


@inspections_bp.route('/<int:inspection_id>/assign-team', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
@swag_from({
    'tags': ['📋 DAT - Inspeções'],
    'summary': 'Aloca equipe e técnico para uma inspeção',
    'description': 'Endpoint específico para alocação rápida de equipe e técnico',
    'parameters': [
        {
            'in': 'path',
            'name': 'inspection_id',
            'required': True,
            'type': 'integer',
            'description': 'ID da inspeção'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'team_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID da equipe responsável'
                    },
                    'technician_id': {
                        'type': 'integer',
                        'example': 5,
                        'description': 'ID do técnico responsável'
                    },
                    'scheduled_date': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-11-15T09:00:00',
                        'description': 'Nova data agendada (opcional)'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Equipe alocada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'inspection': {'type': 'object'}
                }
            }
        },
        400: {
            'description': 'Dados inválidos'
        },
        404: {
            'description': 'Inspeção não encontrada'
        }
    },
    'security': [{'Bearer': []}]
})
def assign_team_to_inspection(inspection_id):
    """Aloca equipe e técnico para uma inspeção"""
    inspection = Inspection.query.get(inspection_id)
    
    if not inspection:
        return jsonify({'error': 'Inspeção não encontrada'}), 404
    
    data = request.get_json()
    
    # Validar equipe se fornecida
    if 'team_id' in data and data['team_id']:
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 400
        inspection.team_id = data['team_id']
    
    # Validar técnico se fornecido
    if 'technician_id' in data and data['technician_id']:
        technician = User.query.get(data['technician_id'])
        if not technician:
            return jsonify({'error': 'Técnico não encontrado'}), 400
        if technician.role != 'tecnico':
            return jsonify({'error': 'Usuário não é um técnico'}), 400
        inspection.technician_id = data['technician_id']
    
    # Atualizar data se fornecida
    if 'scheduled_date' in data:
        try:
            inspection.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
    
    # Atualizar status para "em_andamento" se equipe foi alocada
    if inspection.team_id and inspection.status == Inspection.STATUS_PENDING:
        inspection.status = Inspection.STATUS_IN_PROGRESS
    
    db.session.commit()
    
    return jsonify({
        'message': 'Equipe alocada com sucesso',
        'inspection': inspection.to_dict()
    }), 200


@inspections_bp.route('/<int:inspection_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['📋 DAT - Inspeções'],
    'summary': 'Obtém detalhes de uma inspeção',
    'description': 'Retorna os detalhes completos de uma inspeção específica',
    'parameters': [
        {
            'in': 'path',
            'name': 'inspection_id',
            'required': True,
            'type': 'integer',
            'description': 'ID da inspeção'
        }
    ],
    'responses': {
        200: {
            'description': 'Detalhes da inspeção',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'title': {'type': 'string'},
                    'status': {'type': 'string'},
                    'scheduled_date': {'type': 'string'},
                    'team_id': {'type': 'integer'},
                    'technician_id': {'type': 'integer'}
                }
            }
        },
        404: {
            'description': 'Inspeção não encontrada'
        }
    },
    'security': [{'Bearer': []}]
})
def get_inspection(inspection_id):
    """Obtém detalhes de uma inspeção específica"""
    current_user = get_current_user()
    inspection = Inspection.query.get(inspection_id)
    
    if not inspection:
        return jsonify({'error': 'Inspeção não encontrada'}), 404
    
    # Técnicos só podem ver suas próprias inspeções
    if current_user.role == 'tecnico' and inspection.technician_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    return jsonify(inspection.to_dict()), 200


@inspections_bp.route('', methods=['POST'])
@jwt_required()
@role_required('superadmin', 'admin', 'coord')
@swag_from({
    'tags': ['📋 DAT - Inspeções'],
    'summary': 'Cria uma nova inspeção manualmente',
    'description': 'Permite criar inspeções manualmente com todos os campos necessários, incluindo alocação de equipe',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title', 'scheduled_date', 'client_id'],
                'properties': {
                    'title': {
                        'type': 'string',
                        'example': 'Inspeção Extintor ABC 6kg - Torre Norte'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Inspeção periódica do extintor conforme cronograma'
                    },
                    'scheduled_date': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-11-15T09:00:00'
                    },
                    'client_id': {
                        'type': 'integer',
                        'example': 17
                    },
                    'branch_id': {
                        'type': 'integer',
                        'example': 21
                    },
                    'equipment_id': {
                        'type': 'integer',
                        'example': 16
                    },
                    'contract_id': {
                        'type': 'integer',
                        'example': 16
                    },
                    'team_id': {
                        'type': 'integer',
                        'example': 1
                    },
                    'technician_id': {
                        'type': 'integer',
                        'example': 5
                    },
                    'priority': {
                        'type': 'string',
                        'enum': ['baixa', 'media', 'alta', 'urgente'],
                        'example': 'media'
                    },
                    'location': {
                        'type': 'string',
                        'example': '1º andar - Corredor A'
                    },
                    'equipment': {
                        'type': 'string',
                        'example': 'Extintor ABC 6kg'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Inspeção criada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'inspection': {'type': 'object'}
                }
            }
        },
        400: {
            'description': 'Dados inválidos'
        },
        401: {
            'description': 'Token inválido'
        },
        403: {
            'description': 'Acesso negado'
        }
    },
    'security': [{'Bearer': []}]
})
def create_inspection():
    """Cria uma nova inspeção manualmente"""
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
        return jsonify({'error': 'Formato de data inválido para scheduled_date'}), 400
    
    # Validar cliente existe
    client = Client.query.get(data['client_id'])
    if not client:
        return jsonify({'error': 'Cliente não encontrado'}), 400
    
    # Validar filial se fornecida
    if 'branch_id' in data and data['branch_id']:
        branch = Branch.query.get(data['branch_id'])
        if not branch:
            return jsonify({'error': 'Filial não encontrada'}), 400
        if branch.company_id != data['client_id']:
            return jsonify({'error': 'Filial não pertence ao cliente especificado'}), 400
    
    # Validar equipamento se fornecido
    if 'equipment_id' in data and data['equipment_id']:
        equipment = Equipment.query.get(data['equipment_id'])
        if not equipment:
            return jsonify({'error': 'Equipamento não encontrado'}), 400
    
    # Validar contrato se fornecido
    if 'contract_id' in data and data['contract_id']:
        contract = Contract.query.get(data['contract_id'])
        if not contract:
            return jsonify({'error': 'Contrato não encontrado'}), 400
        if contract.company_id != data['client_id']:
            return jsonify({'error': 'Contrato não pertence ao cliente especificado'}), 400
    
    # Validar equipe se fornecida
    if 'team_id' in data and data['team_id']:
        team = Team.query.get(data['team_id'])
        if not team:
            return jsonify({'error': 'Equipe não encontrada'}), 400
    
    # Validar técnico se fornecido
    if 'technician_id' in data and data['technician_id']:
        technician = User.query.get(data['technician_id'])
        if not technician:
            return jsonify({'error': 'Técnico não encontrado'}), 400
        if technician.role != 'tecnico':
            return jsonify({'error': 'Usuário não é um técnico'}), 400
    
    # Validar prioridade
    if 'priority' in data and data['priority'] not in ['baixa', 'media', 'alta', 'urgente']:
        return jsonify({'error': 'Prioridade inválida'}), 400
    
    # Criar nova inspeção
    inspection = Inspection(
        title=data['title'],
        description=data.get('description'),
        scheduled_date=scheduled_date,
        status=data.get('status', Inspection.STATUS_PENDING),
        priority=data.get('priority', 'media'),
        location=data.get('location'),
        equipment=data.get('equipment'),
        client_id=data['client_id'],
        branch_id=data.get('branch_id'),
        equipment_id=data.get('equipment_id'),
        contract_id=data.get('contract_id'),
        team_id=data.get('team_id'),
        technician_id=data.get('technician_id'),
        created_by=current_user.id
    )
    
    db.session.add(inspection)
    db.session.commit()
    
    return jsonify({
        'message': 'Inspeção criada com sucesso',
        'inspection': inspection.to_dict()
    }), 201


@inspections_bp.route('/<int:inspection_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['📋 DAT - Inspeções'],
    'summary': 'Atualiza uma inspeção existente',
    'description': 'Permite atualizar inspeções, especialmente para alocação de equipes e técnicos',
    'parameters': [
        {
            'in': 'path',
            'name': 'inspection_id',
            'required': True,
            'type': 'integer',
            'description': 'ID da inspeção'
        },
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'example': 'Inspeção Extintor ABC 6kg - Torre Norte'
                    },
                    'description': {
                        'type': 'string',
                        'example': 'Inspeção periódica do extintor conforme cronograma'
                    },
                    'scheduled_date': {
                        'type': 'string',
                        'format': 'date-time',
                        'example': '2025-11-15T09:00:00'
                    },
                    'status': {
                        'type': 'string',
                        'enum': ['pendente', 'em_andamento', 'concluida', 'cancelada'],
                        'example': 'pendente'
                    },
                    'priority': {
                        'type': 'string',
                        'enum': ['baixa', 'media', 'alta', 'urgente'],
                        'example': 'media'
                    },
                    'location': {
                        'type': 'string',
                        'example': '1º andar - Corredor A'
                    },
                    'equipment': {
                        'type': 'string',
                        'example': 'Extintor ABC 6kg'
                    },
                    'team_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID da equipe responsável'
                    },
                    'technician_id': {
                        'type': 'integer',
                        'example': 5,
                        'description': 'ID do técnico responsável'
                    },
                    'branch_id': {
                        'type': 'integer',
                        'example': 21
                    },
                    'equipment_id': {
                        'type': 'integer',
                        'example': 16
                    },
                    'contract_id': {
                        'type': 'integer',
                        'example': 16
                    },
                    'result': {
                        'type': 'string',
                        'example': 'Equipamento em perfeito estado'
                    },
                    'observations': {
                        'type': 'string',
                        'example': 'Nenhuma observação'
                    },
                    'photos': {
                        'type': 'string',
                        'example': '["url1.jpg", "url2.jpg"]'
                    },
                    'signature': {
                        'type': 'string',
                        'example': 'base64_signature_data'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Inspeção atualizada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'inspection': {'type': 'object'}
                }
            }
        },
        400: {
            'description': 'Dados inválidos'
        },
        401: {
            'description': 'Token inválido'
        },
        403: {
            'description': 'Acesso negado'
        },
        404: {
            'description': 'Inspeção não encontrada'
        }
    },
    'security': [{'Bearer': []}]
})
def update_inspection(inspection_id):
    """Atualiza uma inspeção existente"""
    current_user = get_current_user()
    inspection = Inspection.query.get(inspection_id)
    
    if not inspection:
        return jsonify({'error': 'Inspeção não encontrada'}), 404
    
    # Técnicos só podem atualizar suas próprias inspeções
    if current_user.role == 'tecnico' and inspection.technician_id != current_user.id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    # Atualizar campos permitidos baseado no role
    can_edit_all = current_user.has_role('superadmin', 'admin', 'coord')
    
    if 'title' in data and can_edit_all:
        inspection.title = data['title']
    
    if 'description' in data:
        inspection.description = data['description']
    
    if 'scheduled_date' in data and can_edit_all:
        try:
            inspection.scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except ValueError:
            return jsonify({'error': 'Formato de data inválido para scheduled_date'}), 400
    
    if 'status' in data:
        if data['status'] not in Inspection.STATUSES:
            return jsonify({'error': f'Status inválido. Opções: {", ".join(Inspection.STATUSES)}'}), 400
        inspection.status = data['status']
        
        # Atualizar data de conclusão se status for concluída
        if data['status'] == Inspection.STATUS_COMPLETED and not inspection.completed_date:
            inspection.completed_date = datetime.utcnow()
    
    if 'priority' in data and can_edit_all:
        if data['priority'] not in ['baixa', 'media', 'alta', 'urgente']:
            return jsonify({'error': 'Prioridade inválida'}), 400
        inspection.priority = data['priority']
    
    if 'location' in data:
        inspection.location = data['location']
    
    if 'equipment' in data:
        inspection.equipment = data['equipment']
    
    # Validações para alocação de equipe e técnico
    if 'team_id' in data and can_edit_all:
        if data['team_id']:
            team = Team.query.get(data['team_id'])
            if not team:
                return jsonify({'error': 'Equipe não encontrada'}), 400
        inspection.team_id = data['team_id']
    
    if 'technician_id' in data and can_edit_all:
        if data['technician_id']:
            technician = User.query.get(data['technician_id'])
            if not technician:
                return jsonify({'error': 'Técnico não encontrado'}), 400
            if technician.role != 'tecnico':
                return jsonify({'error': 'Usuário não é um técnico'}), 400
        inspection.technician_id = data['technician_id']
    
    # Validações para relacionamentos
    if 'branch_id' in data and can_edit_all:
        if data['branch_id']:
            branch = Branch.query.get(data['branch_id'])
            if not branch:
                return jsonify({'error': 'Filial não encontrada'}), 400
            if branch.company_id != inspection.client_id:
                return jsonify({'error': 'Filial não pertence ao cliente da inspeção'}), 400
        inspection.branch_id = data['branch_id']
    
    if 'equipment_id' in data and can_edit_all:
        if data['equipment_id']:
            equipment = Equipment.query.get(data['equipment_id'])
            if not equipment:
                return jsonify({'error': 'Equipamento não encontrado'}), 400
        inspection.equipment_id = data['equipment_id']
    
    if 'contract_id' in data and can_edit_all:
        if data['contract_id']:
            contract = Contract.query.get(data['contract_id'])
            if not contract:
                return jsonify({'error': 'Contrato não encontrado'}), 400
            if contract.company_id != inspection.client_id:
                return jsonify({'error': 'Contrato não pertence ao cliente da inspeção'}), 400
        inspection.contract_id = data['contract_id']
    
    # Campos de resultado (técnicos podem atualizar)
    if 'result' in data:
        inspection.result = data['result']
    
    if 'observations' in data:
        inspection.observations = data['observations']
    
    if 'photos' in data:
        inspection.photos = data['photos']
    
    if 'signature' in data:
        inspection.signature = data['signature']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Inspeção atualizada com sucesso',
        'inspection': inspection.to_dict()
    }), 200


@inspections_bp.route('/<int:inspection_id>', methods=['DELETE'])
@jwt_required()
@role_required('superadmin', 'admin')
def delete_inspection(inspection_id):
    """Cancela uma inspeção"""
    inspection = Inspection.query.get(inspection_id)
    
    if not inspection:
        return jsonify({'error': 'Inspeção não encontrada'}), 404
    
    inspection.status = Inspection.STATUS_CANCELLED
    db.session.commit()
    
    return jsonify({'message': 'Inspeção cancelada com sucesso'}), 200

