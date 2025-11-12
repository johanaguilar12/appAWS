from flask import request, jsonify
from validators.student_input_validator import validate_student_input
from data.in_memory_storage import students, next_student_id

def get_all_students():
    return jsonify(students), 200

def get_student_by_id(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

def create_student():
    global next_student_id
    data = request.get_json()
    errors = validate_student_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    # Usar el id enviado por el cliente, si existe
    student_id = data.get("id", next_student_id)

    new_student = {
        "id": student_id,
        "nombres": data["nombres"].strip(),
        "apellidos": data["apellidos"].strip(),
        "matricula": data["matricula"],
        "promedio": float(data["promedio"])
    }

    students.append(new_student)

    # Actualizar next_student_id para no generar id duplicado
    next_student_id = max(next_student_id, student_id + 1)

    return jsonify(new_student), 201

def update_student(student_id):
    data = request.get_json()
    errors = validate_student_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    for student in students:
        if student["id"] == student_id:
            student.update({
                "nombres": data["nombres"].strip(),
                "apellidos": data["apellidos"].strip(),
                "matricula": data["matricula"],
                "promedio": float(data["promedio"])
            })
            return jsonify(student), 200

    return jsonify({"error": "Alumno no encontrado"}), 404

def delete_student(student_id):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return jsonify({"message": "Alumno eliminado exitosamente"}), 200
    return jsonify({"error": "Alumno no encontrado"}), 404
