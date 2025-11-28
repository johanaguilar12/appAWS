from extensions import db 

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    teaching_hours = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "numeroEmpleado": self.employee_number,
            "nombres": self.first_name,
            "apellidos": self.last_name,
            "horasClase": self.teaching_hours,
        }