from flask import Blueprint
from controllers.student_management_controller import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)

student_blueprint = Blueprint("students", __name__, url_prefix="/alumnos")

student_blueprint.route("", methods=["GET"])(get_all_students)
student_blueprint.route("/<int:student_id>", methods=["GET"])(get_student_by_id)
student_blueprint.route("", methods=["POST"])(create_student)
student_blueprint.route("/<int:student_id>", methods=["PUT"])(update_student)
student_blueprint.route("/<int:student_id>", methods=["DELETE"])(delete_student)
