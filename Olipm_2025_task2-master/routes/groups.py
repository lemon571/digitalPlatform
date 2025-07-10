from flask import Blueprint, request, jsonify, abort
from models import db, Group
from flasgger import swag_from

groups_bp = Blueprint('groups', __name__)


@groups_bp.route('/groups', methods=['POST'])
@swag_from({
    "parameters": [
        {"name": "body", "in": "body", "required": True,
         "schema": {"id": "Group", "properties": {"name": {"type": "string"}, "parent_id": {"type": "integer"}}}}
    ],
    "responses": {201: {"description": "Group created"}}
})
def create_group():
    data = request.json
    group = Group(name=data['name'], parent_id=data.get('parent_id'))
    db.session.add(group)
    db.session.commit()
    return jsonify({'id': group.id, 'parent_id': group.parent_id, 'name': group.name}), 201


@groups_bp.route('/groups', methods=['GET'])
@swag_from({"responses": {200: {"description": "List groups"}}})
def get_groups():
    groups = Group.query.all()
    return jsonify(
        [{'id': g.id, 'name': g.name, 'subGroups': [{'id': sg.id, 'name': sg.name} for sg in g.subgroups]} for g in
         groups])


@groups_bp.route('/groups/<int:id>', methods=['GET'])
@swag_from({
    "parameters": [
        {"name": "id", "in": "path", "type": "integer", "required": True, "description": "ID of the group"}
    ],
    "responses": {200: {"description": "Group details"}, 404: {"description": "Group not found"}}
})
def get_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, description=f"Group with id {id} not found")
    return jsonify({'id': group.id, 'name': group.name})


@groups_bp.route('/groups/<int:id>', methods=['PUT'])
@swag_from({
    "parameters": [
        {"name": "id", "in": "path", "type": "integer", "required": True, "description": "ID of the group"},
        {"name": "body", "in": "body", "required": True,
         "schema": {"id": "GroupUpdate", "properties": {"name": {"type": "string"}, "parent_id": {"type": "integer"}}}}
    ],
    "responses": {200: {"description": "Group updated"}, 404: {"description": "Group not found"}}
})
def update_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, description=f"Group with id {id} not found")
    data = request.json
    group.name = data.get('name', group.name)
    group.parent_id = data.get('parent_id', group.parent_id)
    db.session.commit()
    return jsonify({'id': group.id, 'parent_id': group.parent_id, 'name': group.name})


@groups_bp.route('/groups/<int:id>', methods=['DELETE'])
@swag_from({
    "parameters": [
        {"name": "id", "in": "path", "type": "integer", "required": True, "description": "ID of the group"}
    ],
    "responses": {200: {"description": "Group deleted"}, 400: {"description": "Group has subgroups, cannot delete."},
                  404: {"description": "Group not found"}}
})
def delete_group(id):
    group = Group.query.get(id)
    if not group:
        abort(404, description=f"Group with id {id} not found")
    if group.subgroups:
        abort(400, description='Group has subgroups, cannot delete.')
    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
