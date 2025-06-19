from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Divide una stringa in una lista usando il delimitatore specificato"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]

@register.filter
def trim(value):
    """Rimuove spazi bianchi all'inizio e alla fine della stringa"""
    if not value:
        return ''
    return str(value).strip()

@register.filter
def format_event_dates(date_list):
    """Formatta la lista di date degli eventi in modo leggibile"""
    if not date_list:
        return ''

    # Se è una singola data
    if len(date_list) == 1:
        return date_list[0]

    # Se sono più date consecutive
    if len(date_list) == 2:
        return f"Dal {date_list[0]} al {date_list[1]}"

    # Se sono più di due date
    return f"Dal {date_list[0]} al {date_list[-1]} ({len(date_list)} giorni)"

@register.filter
def clean_hashtags(value):
    """Rimuove i simboli # dai tag se presenti"""
    if not value:
        return ''
    return str(value).replace('#', '').strip()

@register.filter
def truncate_smart(value, length=15):
    """Tronca il testo a un numero specifico di parole mantenendo la punteggiatura"""
    if not value:
        return ''

    words = str(value).split()
    if len(words) <= length:
        return value

    truncated = ' '.join(words[:length])
    return f"{truncated}..."

@register.filter
def format_author_list(authors_list):
    """Formatta la lista degli autori in modo leggibile"""
    if not authors_list:
        return ''

    if len(authors_list) == 1:
        return authors_list[0]
    elif len(authors_list) == 2:
        return f"{authors_list[0]} e {authors_list[1]}"
    else:
        return f"{', '.join(authors_list[:-1])} e {authors_list[-1]}"
