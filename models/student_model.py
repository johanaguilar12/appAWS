from extensions import db  

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    registration_number = db.Column(db.String(10), nullable=False)
    grade_average = db.Column(db.Float, nullable=False)
    foto_perfil_url = db.Column(db.String(255)) 
    password = db.Column(db.String(100)) 

    def to_dict(self):
        return {
            "id": self.id,
            "nombres": self.first_name,
            "apellidos": self.last_name,
            "matricula": self.registration_number,
            "promedio": self.grade_average,
            "fotoPerfilUrl": self.foto_perfil_url
        }