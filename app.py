from flask import Flask
from extensions import db  
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    if db_user and db_host:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_test.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from routes.student_routes import student_blueprint
        from routes.teacher_routes import teacher_blueprint
        
        import models.student_model
        import models.teacher_model

        db.create_all()

        app.register_blueprint(student_blueprint)
        app.register_blueprint(teacher_blueprint)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
