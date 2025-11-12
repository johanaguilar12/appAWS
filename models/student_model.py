from typing import Dict

class Student:
    def __init__(
        self,
        student_id: int,
        first_name: str,
        last_name: str,
        registration_number: int,  # matrícula numérica de 8 dígitos
        grade_average: float,      # promedio 0.0 - 100.0
    ) -> None:
        self.id: int = student_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.registration_number: int = registration_number
        self.grade_average: float = grade_average

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "nombres": self.first_name,
            "apellidos": self.last_name,
            "matricula": self.registration_number,
            "promedio": self.grade_average,
        }