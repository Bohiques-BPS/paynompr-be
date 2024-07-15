def time_to_minutes(time_str: str) -> int:
    """Convierte una cadena de tiempo en formato HH:MM a minutos."""
    if not time_str:
        return 0
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def minutes_to_time(minutes: int) -> str:
    """Convierte minutos a una cadena de tiempo en formato HH:MM."""
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}"
