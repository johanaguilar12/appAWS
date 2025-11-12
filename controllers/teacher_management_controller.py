from flask import request, jsonify
from validators.teacher_input_validator import validate_teacher_input
from data.in_memory_storage import teachers, next_teacher_id

def get_all_teachers():
    return jsonify(teachers), 200

def get_teacher_by_id(teacher_id):
    for teacher in teachers:
        if teacher["id"] == teacher_id:
            return jsonify(teacher), 200
    return jsonify({"error": "Profesor no encontrado"}), 404

def create_teacher():
    global next_teacher_id
    data = request.get_json()
    errors = validate_teacher_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    teacher_id = data.get("id", next_teacher_id)

    new_teacher = {
        "id": teacher_id,
        "nombres": data["nombres"].strip(),
        "apellidos": data["apellidos"].strip(),
        "numeroEmpleado": int(data["numeroEmpleado"]),
        "horasClase": int(float(data["horasClase"]))
    }

    teachers.append(new_teacher)
    next_teacher_id = max(next_teacher_id, teacher_id + 1)
    return jsonify(new_teacher), 201

def update_teacher(teacher_id):
    data = request.get_json()
    errors = validate_teacher_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    for teacher in teachers:
        if teacher["id"] == teacher_id:
            teacher.update({
                "nombres": data["nombres"].strip(),
                "apellidos": data["apellidos"].strip(),
                "numeroEmpleado": int(data["numeroEmpleado"]),
                "horasClase": int(float(data["horasClase"]))
            })
            return jsonify(teacher), 200

    return jsonify({"error": "Profesor no encontrado"}), 404

def delete_teacher(teacher_id):
    for teacher in teachers:
        if teacher["id"] == teacher_id:
            teachers.remove(teacher)
            return jsonify({"message": "Profesor eliminado exitosamente"}), 200
    return jsonify({"error": "Profesor no encontrado"}), 404
