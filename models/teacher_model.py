from typing import Dict

class Teacher:
    def __init__(
        self,
        teacher_id: int,
        employee_number: int,  # número de empleado
        first_name: str,
        last_name: str,
        teaching_hours: int,   # horas de clase (solo enteras)
    ) -> None:
        self.id: int = teacher_id
        self.employee_number: int = employee_number
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.teaching_hours: int = teaching_hours

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "numeroEmpleado": self.employee_number,
            "nombres": self.first_name,
            "apellidos": self.last_name,
            "horasClase": self.teaching_hours,
        }