from flask import Blueprint, request, jsonify, abort
from models import db, Student, Group
from flasgger import swag_from
from sqlalchemy import or_

students_bp = Blueprint('students', __name__)


@students_bp.route('/students', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "id": "Student",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "group_id": {"type": "integer"}
                },
                "required": ["name", "email", "group_id"]
            }
        }
    ],
    "responses": {
        201: {"description": "Student created"},
        400: {"description": "Group does not exist or email is not unique"},
        409: {"description": "Email already exists"}
    }
})
def create_student():
    data = request.json
    group = Group.query.get(data['group_id'])
    if not group:
        abort(400, description=f"Group with id {data['group_id']} does not exist")
    try:
        student = Student(name=data['name'], email=data['email'], group_id=data['group_id'])
        db.session.add(student)
        db.session.commit()
        return jsonify({'id': student.id, 'group_id': student.group_id, 'name': student.name}), 201
    except Exception as e:
        db.session.rollback()
        if 'unique constraint' in str(e) or 'duplicate key value' in str(e):
            abort(409, description=f"Email already exists: {data['email']}")
        abort(400, description=f"Error creating student: {e}")


@students_bp.route('/students', methods=['GET'])
@swag_from({"responses": {200: {"description": "List students"}}})
def get_students():
    query = request.args.get('query')
    students_query = Student.query
    if query:
        students_query = students_query.join(Group, Student.group_id == Group.id).filter(
            db.or_(Student.name.ilike(f'%{query}%'), Group.name.ilike(f'%{query}%')))
    students = students_query.all()
    return jsonify([{'id': s.id, 'group_id': s.group_id, 'name': s.name} for s in students])


@students_bp.route('/students/<int:id>', methods=['GET'])
@swag_from({
    "parameters": [{
        "name": "id",
        "in": "path",
        "type": "integer",
        "required": True,
        "description": "ID of the student to get"
    }],
    "responses": {200: {"description": "Student details"}, 404: {"description": "Student not found"}}})
def get_student(id):
    student = Student.query.get(id)
    if not student:
        abort(404, description=f"Student with id {id} not found")
    return jsonify({'id': student.id, 'group_id': student.group_id, 'name': student.name})


@students_bp.route('/students/<int:id>', methods=['PUT'])
@swag_from({
    "parameters": [{
        "name": "id",
        "in": "path",
        "type": "integer",
        "required": True,
        "description": "ID of the student to update"
    },
        {"name": "body", "in": "body", "required": True,
         "schema": {"id": "StudentUpdate", "properties": {"name": {"type": "string"}, "group_id": {"type": "integer"}}}}
    ],
    "responses": {200: {"description": "Student updated"}, 400: {"description": "Group does not exist"},
                  404: {"description": "Student not found"}}
})
def update_student(id):
    student = Student.query.get(id)
    if not student:
        abort(404, description=f"Student with id {id} not found")
    data = request.json
    if 'group_id' in data:
        group = Group.query.get(data['group_id'])
        if not group:
            abort(400, description=f"Group with id {data['group_id']} does not exist")
        student.group_id = data['group_id']
    student.name = data.get('name', student.name)
    db.session.commit()
    return jsonify({'id': student.id, 'group_id': student.group_id, 'name': student.name})


@students_bp.route('/students/<int:id>', methods=['DELETE'])
@swag_from({
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the student to delete"
        }
    ],
    "responses": {
        200: {"description": "Student deleted"},
        404: {"description": "Student not found"}
    }
})
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        abort(404, description=f"Student with id {id} not found")
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Deleted successfully'}), 200
