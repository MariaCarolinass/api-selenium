from datetime import datetime, timedelta

def get_previous_month_info():
    today = datetime.now()
    first_day_current = today.replace(day=1)
    last_day_previous = first_day_current - timedelta(days=1)

    return {
        'month': last_day_previous.month,
        'year': last_day_previous.year,
        'month_pt': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][last_day_previous.month - 1]
    }

def is_from_previous_month(text, previous_month_info):
    if not text:
        return True
        
    text_lower = text.lower()
    month_indicators = [
        previous_month_info['month_pt'],
        f"{previous_month_info['month']:02d}",
        str(previous_month_info['year'])
    ]
    
    return any(indicator in text_lower for indicator in month_indicators)

def clean_filename(text):
    if not text:
        return ""
    filename = "".join(c for c in text if c.isalnum() or c in (' ', '-', '_')).rstrip()
    return filename[:50]

def generate_filename(title, index):
    clean_title = clean_filename(title).replace(' ', '_')[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"DOM_{clean_title}_{index+1:02d}_{timestamp}.pdf"