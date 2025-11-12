from flask import Flask
from routes.student_routes import student_blueprint
from routes.teacher_routes import teacher_blueprint

app = Flask(__name__)

# Registrar blueprints
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
