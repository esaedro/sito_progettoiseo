from __future__ import annotations

import html as py_html
from html.parser import HTMLParser
from typing import Iterable
from urllib.parse import urlparse

try:
    import bleach  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    bleach = None


ALLOWED_TAGS: list[str] = [
    "p",
    "br",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "ul",
    "ol",
    "li",
    "a",
]

ALLOWED_ATTRS: dict[str, list[str]] = {
    "a": ["href", "title", "target", "rel"],
}

ALLOWED_PROTOCOLS: set[str] = {"http", "https", "mailto"}


def maybe_unescape_html(value: str) -> str:
    """Se il testo sembra HTML-escaped (es. &lt;p&gt;), fa un unescape singolo."""
    if "<" not in value and ("&lt;" in value or "&#60;" in value or "&#x3c;" in value.lower()):
        return py_html.unescape(value)
    return value


def _is_safe_href(href: str) -> bool:
    href = (href or "").strip()
    if not href:
        return False

    parsed = urlparse(href)
    scheme = (parsed.scheme or "").lower()

    # URL relativo (no scheme) -> ok
    if not scheme:
        return True

    return scheme in ALLOWED_PROTOCOLS


class _SimpleHTMLSanitizer(HTMLParser):
    def __init__(self, allowed_tags: set[str]):
        super().__init__(convert_charrefs=True)
        self._allowed_tags = allowed_tags
        self._out: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag = tag.lower()
        if tag not in self._allowed_tags:
            return

        if tag == "br":
            self._out.append("<br>")
            return

        if tag == "a":
            attr_map = {k.lower(): (v or "") for k, v in attrs}
            href = attr_map.get("href", "")
            if not _is_safe_href(href):
                # Link non sicuro -> degradalo a testo (non aggiungere il tag)
                return

            title = attr_map.get("title", "")
            target = attr_map.get("target", "")
            rel = attr_map.get("rel", "")

            safe_attrs: list[str] = [f'href="{py_html.escape(href, quote=True)}"']
            if title:
                safe_attrs.append(f'title="{py_html.escape(title, quote=True)}"')

            if target:
                safe_target = "_blank" if target == "_blank" else ""
                if safe_target:
                    safe_attrs.append('target="_blank"')
                    # Forza rel sicuro se target _blank
                    rel_tokens = {t.strip().lower() for t in rel.split() if t.strip()}
                    rel_tokens.update({"noopener", "noreferrer"})
                    safe_attrs.append(f'rel="{py_html.escape(" ".join(sorted(rel_tokens)), quote=True)}"')
            self._out.append(f"<a {' '.join(safe_attrs)}>")
            return

        # Tag generico senza attributi
        self._out.append(f"<{tag}>")

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag not in self._allowed_tags:
            return
        if tag == "br":
            return
        self._out.append(f"</{tag}>")

    def handle_data(self, data: str):
        if not data:
            return
        self._out.append(py_html.escape(data))

    def get_html(self) -> str:
        return "".join(self._out)


def sanitize_rich_text(value: str) -> str:
    """Sanitizza rich text proveniente dal WYSIWYG.

    - Supporta contenuto HTML già escaped (es. &lt;p&gt;...)
    - Se è plain-text, preserva newline come <br>
    - Se `bleach` è disponibile: usa bleach
    - Altrimenti: fallback con sanitizer interno (tag whitelist)
    """
    value = (value or "").strip()
    if not value:
        return ""

    value = maybe_unescape_html(value)

    # Plain text -> escape + <br>
    if "<" not in value and ">" not in value:
        escaped = py_html.escape(value)
        escaped = escaped.replace("\r\n", "\n").replace("\r", "\n")
        return escaped.replace("\n", "<br>")

    if bleach is not None:
        return bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=list(ALLOWED_PROTOCOLS),
            strip=True,
        )

    sanitizer = _SimpleHTMLSanitizer(set(ALLOWED_TAGS))
    sanitizer.feed(value)
    sanitizer.close()
    return sanitizer.get_html()
