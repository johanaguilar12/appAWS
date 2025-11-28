import boto3, uuid, time, secrets, os
from flask import request, jsonify
from extensions import db
from models.student_model import Student
from validators.student_input_validator import validate_student_input
from dotenv import load_dotenv


load_dotenv()

# --- CONFIGURACIÓN AWS ---
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
DYNAMO_TABLE_NAME = os.getenv('DYNAMO_TABLE_NAME')

# Clientes de AWS
s3_client = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

sns_client = boto3.client(
    'sns',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

def get_all_students():
    try:
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students]), 200
    except Exception as e:
        return jsonify({"error": "Error de conexión a BD"}), 500

def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({"error": "Alumno no encontrado"}), 404

def create_student():
    data = request.get_json()
    errors = validate_student_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    new_student = Student(
        first_name=data["nombres"].strip(),
        last_name=data["apellidos"].strip(),
        registration_number=data["matricula"],
        grade_average=float(data["promedio"]),
        password=data.get("password", "123456") 
    )

    try:
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def update_student(student_id):
    data = request.get_json()
    errors = validate_student_input(data)
    if errors:
        return jsonify({"errors": errors}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Alumno no encontrado"}), 404

    student.first_name = data["nombres"].strip()
    student.last_name = data["apellidos"].strip()
    student.registration_number = data["matricula"]
    student.grade_average = float(data["promedio"])
    if "password" in data:
        student.password = data["password"]

    try:
        db.session.commit()
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Alumno no encontrado"}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Alumno eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- AWS INTEGRATIONS ---
def upload_profile_picture(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Alumno no encontrado"}), 404

    if 'foto' not in request.files:
        return jsonify({"error": "No se proporcionó el archivo 'foto'"}), 400

    file = request.files['foto']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    file_key = f"alumnos/{student_id}/{file.filename}"

    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET_NAME,
            file_key,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            }
        )

        foto_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
        student.foto_perfil_url = foto_url
        db.session.commit()

        return jsonify({"url": foto_url}), 200

    except Exception as e:
        return jsonify({"error": f"Error al subir a S3: {str(e)}"}), 500

def send_email_notification(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Alumno no encontrado"}), 404

    message_body = (
        f"Hola,\n\n"
        f"Se reportan las siguientes calificaciones para el alumno:\n"
        f"Nombre: {student.first_name} {student.last_name}\n"
        f"Matrícula: {student.registration_number}\n"
        f"Promedio General: {student.grade_average}\n"
    )

    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message_body,
            Subject=f"Reporte de Calificaciones - {student.first_name}"
        )
        return jsonify({"message": "Notificación enviada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error enviando SNS: {str(e)}"}), 500

def login_student(student_id):
    data = request.get_json()
    password_input = data.get("password")

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Alumno no encontrado"}), 404

    if student.password != password_input:
        return jsonify({"error": "Contraseña incorrecta"}), 403

    session_string = secrets.token_hex(64) # 128 chars

    table = dynamodb.Table(DYNAMO_TABLE_NAME)
    
    item = {
        'id': str(uuid.uuid4()),
        'fecha': int(time.time()),
        'alumnoId': student_id,
        'active': True,
        'sessionString': session_string
    }

    try:
        table.put_item(Item=item)
        return jsonify({"sessionString": session_string}), 200
    except Exception as e:
        return jsonify({"error": f"Error en DynamoDB: {str(e)}"}), 500

def verify_session(student_id):
    data = request.get_json()
    session_string = data.get("sessionString")

    if not session_string:
        return jsonify({"error": "Falta sessionString"}), 400

    table = dynamodb.Table(DYNAMO_TABLE_NAME)

    try:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('sessionString').eq(session_string) & 
                             boto3.dynamodb.conditions.Attr('alumnoId').eq(student_id)
        )
        
        items = response.get('Items', [])
        
        if items:
            session = items[0]
            if session.get('active') is True:
                return jsonify({"message": "Sesión válida"}), 200
        
        return jsonify({"error": "Sesión inválida o inactiva"}), 400

    except Exception as e:
        return jsonify({"error": f"Error verificando sesión: {str(e)}"}), 500

def logout_student(student_id):
    data = request.get_json()
    session_string = data.get("sessionString")
    table = dynamodb.Table(DYNAMO_TABLE_NAME)

    try:
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('sessionString').eq(session_string)
        )
        items = response.get('Items', [])

        if items:
            session_item_id = items[0]['id']
            
            table.update_item(
                Key={'id': session_item_id},
                UpdateExpression="set active = :val",
                ExpressionAttributeValues={':val': False}
            )
            return jsonify({"message": "Sesión cerrada exitosamente"}), 200
            
        return jsonify({"error": "Sesión no encontrada"}), 404

    except Exception as e:
        return jsonify({"error": f"Error al cerrar sesión: {str(e)}"}), 500