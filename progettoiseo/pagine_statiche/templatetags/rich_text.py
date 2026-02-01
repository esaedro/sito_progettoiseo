from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from progettoiseo.rich_text import sanitize_rich_text

register = template.Library()


@register.filter(name="rich_text")
def rich_text(value: object) -> str:
    """Renderizza rich-text (HTML) in modo sicuro."""
    text = "" if value is None else str(value)
    cleaned = sanitize_rich_text(text)
    return mark_safe(cleaned)
