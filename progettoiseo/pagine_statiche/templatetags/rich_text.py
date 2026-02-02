from __future__ import annotations

import re

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from progettoiseo.rich_text import maybe_unescape_html, sanitize_rich_text

register = template.Library()


@register.filter(name="rich_text")
def rich_text(value: object) -> str:
    """Renderizza rich-text (HTML) in modo sicuro."""
    text = "" if value is None else str(value)
    cleaned = sanitize_rich_text(text)
    return mark_safe(cleaned)


_RE_BR = re.compile(r"(?is)<\s*br\s*/?\s*>")
_RE_P_CLOSE = re.compile(r"(?is)</\s*p\s*>")
_RE_LI_OPEN = re.compile(r"(?is)<\s*li\b[^>]*>")
_RE_LI_CLOSE = re.compile(r"(?is)</\s*li\s*>")
_RE_UL_OPEN = re.compile(r"(?is)<\s*ul\b[^>]*>")
_RE_UL_CLOSE = re.compile(r"(?is)</\s*ul\s*>")
_RE_OL_OPEN = re.compile(r"(?is)<\s*ol\b[^>]*>")
_RE_OL_CLOSE = re.compile(r"(?is)</\s*ol\s*>")


@register.filter(name="plain_text_preview")
def plain_text_preview(value: object) -> str:
    """Estratto testo *senza* formattazione.

    Obiettivo: per le card/preview vogliamo solo testo (niente <a>, <b>, ecc.),
    ma se nel contenuto l'utente va a capo (es. <p> o <br>) vogliamo evitare
    che le parole di righe/paragrafi diversi vengano "incollate" tra loro.
    In preview gli a-capo vengono convertiti in un semplice spazio.
    """
    text = "" if value is None else str(value)
    if not text:
        return ""

    text = maybe_unescape_html(text)

    # Inserisce newline *prima* di strip_tags, così i tag di struttura
    # non vengono "incollati" tra loro (es. </p><p>).
    text = _RE_BR.sub("\n", text)
    text = _RE_P_CLOSE.sub("\n\n", text)

    # Liste: separa gli elementi tra loro e dal resto del testo.
    text = _RE_UL_OPEN.sub("\n", text)
    text = _RE_OL_OPEN.sub("\n", text)
    text = _RE_LI_OPEN.sub("\n", text)
    text = _RE_LI_CLOSE.sub("\n", text)
    text = _RE_UL_CLOSE.sub("\n", text)
    text = _RE_OL_CLOSE.sub("\n", text)

    plain = strip_tags(text)
    plain = plain.replace("\r\n", "\n").replace("\r", "\n")
    # Collassa tutti gli spazi (inclusi newline) in un singolo spazio
    plain = re.sub(r"\s+", " ", plain).strip()
    if not plain:
        return ""

    return plain
