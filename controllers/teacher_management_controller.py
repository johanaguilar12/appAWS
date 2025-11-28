from flask import request, jsonify
from extensions import db 
from models.teacher_model import Teacher
from validators.teacher_input_validator import validate_teacher_input

def get_all_teachers():
    teachers_list = Teacher.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers_list]), 200

def get_teacher_by_id(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if teacher:
        return jsonify(teacher.to_dict()), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

def create_teacher():
    data = request.get_json()
    errors = validate_teacher_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_teacher = Teacher(
        first_name=data["nombres"].strip(),
        last_name=data["apellidos"].strip(),
        employee_number=int(data["numeroEmpleado"]),
        teaching_hours=int(float(data["horasClase"]))
    )

    try:
        db.session.add(new_teacher)   
        db.session.commit()           
        return jsonify(new_teacher.to_dict()), 201
    except Exception as e:
        db.session.rollback()         
        return jsonify({"error": str(e)}), 500

def update_teacher(teacher_id):
    data = request.get_json()
    errors = validate_teacher_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    teacher.first_name = data["nombres"].strip()
    teacher.last_name = data["apellidos"].strip()
    teacher.employee_number = int(data["numeroEmpleado"])
    teacher.teaching_hours = int(float(data["horasClase"]))

    try:
        db.session.commit() 
        return jsonify(teacher.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def delete_teacher(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return jsonify({"error": "Profesor no encontrado"}), 404

    try:
        db.session.delete(teacher) 
        db.session.commit()        
        return jsonify({"message": "Profesor eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500