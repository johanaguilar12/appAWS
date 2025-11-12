from flask import Blueprint
from controllers.teacher_management_controller import (
    get_all_teachers,
    get_teacher_by_id,
    create_teacher,
    update_teacher,
    delete_teacher
)

teacher_blueprint = Blueprint("teachers", __name__, url_prefix="/profesores")

teacher_blueprint.route("", methods=["GET"])(get_all_teachers)
teacher_blueprint.route("/<int:teacher_id>", methods=["GET"])(get_teacher_by_id)
teacher_blueprint.route("", methods=["POST"])(create_teacher)
teacher_blueprint.route("/<int:teacher_id>", methods=["PUT"])(update_teacher)
teacher_blueprint.route("/<int:teacher_id>", methods=["DELETE"])(delete_teacher)
