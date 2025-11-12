def validate_teacher_input(data):
    errors = []

    # nombres y apellidos obligatorios y no vacíos
    if not data.get("nombres") or not isinstance(data["nombres"], str) or not data["nombres"].strip():
        errors.append("El nombre es obligatorio y debe ser un texto válido.")
    if not data.get("apellidos") or not isinstance(data["apellidos"], str) or not data["apellidos"].strip():
        errors.append("Los apellidos son obligatorios y deben ser un texto válido.")

    # numeroEmpleado: número entero positivo
    try:
        numero = int(data.get("numeroEmpleado"))
        if numero <= 0:
            errors.append("El número de empleado debe ser un entero positivo.")
    except:
        errors.append("El número de empleado debe ser un entero válido.")

    # horasClase: número entero positivo
    try:
        horas = float(data.get("horasClase"))
        if horas < 0:
            errors.append("Las horas de clase deben ser positivas.")
    except:
        errors.append("Las horas de clase deben ser un número válido.")

    return errors
