def validate_student_input(data):
    errors = []

    if not data.get("nombres") or not data["nombres"].strip():
        errors.append("Nombre obligatorio.")
    if not data.get("apellidos") or not data["apellidos"].strip():
        errors.append("Apellidos obligatorios.")
    matricula = str(data.get("matricula") or "")
    if not matricula.startswith("A"):
        errors.append("Matrícula inválida.")
    try:
        promedio = float(data.get("promedio"))
        if promedio < 0:
            errors.append("Promedio inválido.")
    except:
        errors.append("Promedio inválido.")

    return errors
