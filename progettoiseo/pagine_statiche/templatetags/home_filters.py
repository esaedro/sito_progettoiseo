from __future__ import annotations

from html.parser import HTMLParser

from django import template

from progettoiseo.rich_text import maybe_unescape_html

register = template.Library()


class _HtmlToPreviewText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs):
        tag = (tag or "").lower()
        if tag in {"p", "div"}:
            self._parts.append("\n")
        elif tag == "br":
            self._parts.append("\n")
        elif tag in {"ul", "ol"}:
            self._parts.append("\n")
        elif tag == "li":
            self._parts.append("\n• ")

    def handle_endtag(self, tag: str):
        tag = (tag or "").lower()
        if tag in {"p", "div", "li"}:
            self._parts.append("\n")

    def handle_data(self, data: str):
        if data:
            self._parts.append(data)

    def get_text(self) -> str:
        return "".join(self._parts)


@register.filter
def rich_preview(value: str) -> str:
    """Converte HTML rich text in testo semplice per anteprime.

    - Rimuove i tag
    - Inserisce separatori per paragrafi/a-capo
    - Rende gli <li> come punti elenco (•)
    """
    if not value:
        return ""

    raw = maybe_unescape_html(str(value))
    parser = _HtmlToPreviewText()
    parser.feed(raw)
    parser.close()

    text = parser.get_text().replace("\r\n", "\n").replace("\r", "\n")
    # In home vogliamo un'anteprima su una riga: usa spazi come separatori.
    return " ".join(text.split())

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
