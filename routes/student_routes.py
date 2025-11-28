from flask import Blueprint
from controllers.student_management_controller import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student,
    upload_profile_picture,   
    send_email_notification,  
    login_student,            
    verify_session,           
    logout_student            
)

student_blueprint = Blueprint("students", __name__, url_prefix="/alumnos")

student_blueprint.route("", methods=["GET"])(get_all_students)
student_blueprint.route("/<int:student_id>", methods=["GET"])(get_student_by_id)
student_blueprint.route("", methods=["POST"])(create_student)
student_blueprint.route("/<int:student_id>", methods=["PUT"])(update_student)
student_blueprint.route("/<int:student_id>", methods=["DELETE"])(delete_student)

# S3: Subir foto de perfil
student_blueprint.route("/<int:student_id>/fotoPerfil", methods=["POST"])(upload_profile_picture)

# SNS: Enviar notificación por correo
student_blueprint.route("/<int:student_id>/email", methods=["POST"])(send_email_notification)

# DynamoDB: Gestión de sesiones
student_blueprint.route("/<int:student_id>/session/login", methods=["POST"])(login_student)
student_blueprint.route("/<int:student_id>/session/verify", methods=["POST"])(verify_session)
student_blueprint.route("/<int:student_id>/session/logout", methods=["POST"])(logout_student)