from datetime import date

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

def getPeriodTime(periodo: int, year: int):
    period = {
        1: {
            'start_date': date(year, 1, 1),
            'end_date': date(year, 3, 31)
        },
        2: {
            'start_date': date(year, 4, 1),
            'end_date': date(year, 6, 30)
        },
        3: {
            'start_date': date(year, 7, 1),
            'end_date': date(year, 9, 30)
        },
        4: {
            'start_date': date(year, 10, 1),
            'end_date': date(year, 12, 31)
        }
    }

    return period[periodo]
