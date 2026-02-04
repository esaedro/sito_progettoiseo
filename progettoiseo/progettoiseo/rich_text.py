from __future__ import annotations

import html as py_html
import re
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

# Match URL/email "semplici" in testo. La logica di normalizzazione gestisce
# schema mancante e punteggiatura finale.
_RE_AUTO_LINK = re.compile(
    r"(?P<email>[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})"
    r"|(?P<url>(?:https?://|www\.)[^\s<]+|[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)+(?:/[^\s<]*)?)",
    flags=re.IGNORECASE,
)

_TRAILING_PUNCTUATION = ".,;:!?)]}›»\"'"

_RE_A_HREF = re.compile(r'(<a\b[^>]*\shref=")([^"]*)("[^>]*>)', flags=re.IGNORECASE)


def _normalize_href(href: str) -> str:
    href = (href or "").strip()
    if not href:
        return ""

    # Già relativo/anchor/query: non toccare
    if href.startswith(("/", "#", "?")):
        return href

    # Protocol-relative
    if href.startswith("//"):
        return f"https:{href}"

    parsed = urlparse(href)
    scheme = (parsed.scheme or "").lower()
    if scheme:
        return href

    # Email senza mailto:
    if "@" in href and " " not in href and not href.lower().startswith("mailto:"):
        return f"mailto:{href}"

    # Domain-like senza schema (tipico quando si usa il tool link del WYSIWYG con www...)
    # Evita di trasformare anchor/relative già gestiti sopra.
    host = href.split("/", 1)[0].split(":", 1)[0]
    if "." in host:
        tld = host.rsplit(".", 1)[-1].lower()
        # Piccola whitelist/blacklist per evitare di scambiare file-type per TLD
        if 2 <= len(tld) <= 10 and tld not in {"html", "htm", "php", "asp", "aspx", "jsp", "txt", "pdf", "png", "jpg", "jpeg", "gif", "svg", "zip"}:
            return f"https://{href}"

    return href


def _linkify_plain_text_to_html(text: str) -> str:
    """Trasforma URL/email in link HTML sicuri, escapando tutto il resto."""
    if not text:
        return ""

    out: list[str] = []
    last = 0
    for m in _RE_AUTO_LINK.finditer(text):
        start, end = m.span()
        if start > last:
            out.append(py_html.escape(text[last:start]))

        token = text[start:end]
        trailing = ""
        while token and token[-1] in _TRAILING_PUNCTUATION:
            trailing = token[-1] + trailing
            token = token[:-1]

        if token:
            href = _normalize_href(token)
            if href:
                out.append(
                    f'<a href="{py_html.escape(href, quote=True)}">{py_html.escape(token)}</a>'
                )
            else:
                out.append(py_html.escape(token))

        if trailing:
            out.append(py_html.escape(trailing))

        last = end

    if last < len(text):
        out.append(py_html.escape(text[last:]))
    return "".join(out)


def _normalize_anchor_hrefs_in_html(html: str) -> str:
    """Normalizza solo gli href dei tag <a> presenti, senza alterare altro HTML."""
    if not html:
        return html

    def _repl(m: re.Match[str]) -> str:
        prefix, href_raw, suffix = m.group(1), m.group(2), m.group(3)
        href_unescaped = py_html.unescape(href_raw)
        normalized = _normalize_href(href_unescaped)
        if normalized == href_unescaped:
            return m.group(0)
        return f"{prefix}{py_html.escape(normalized, quote=True)}{suffix}"

    return _RE_A_HREF.sub(_repl, html)


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
            href = _normalize_href(attr_map.get("href", ""))
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
        # Fallback linkify: se bleach non è disponibile, rendi comunque cliccabili
        # URL/email presenti nel testo.
        if bleach is None:
            self._out.append(_linkify_plain_text_to_html(data))
        else:
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

    def _linkify_if_available(html: str) -> str:
        if bleach is None:
            return html
        def _allow_only_safe_protocols(attrs: dict[str, str], new: bool = False) -> dict[str, str] | None:
            href = (attrs.get("href") or "").strip()
            parsed = urlparse(href)
            scheme = (parsed.scheme or "").lower()
            if scheme and scheme not in ALLOWED_PROTOCOLS:
                return None
            return attrs

        # Trasforma URL/email in <a> senza toccare link già presenti.
        linked = bleach.linkify(
            html,
            skip_tags=["a"],
            parse_email=True,
            callbacks=[_allow_only_safe_protocols],
        )
        return _normalize_anchor_hrefs_in_html(linked)

    # Plain text -> escape + <br>
    if "<" not in value and ">" not in value:
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        if bleach is None:
            # Mantiene le righe con <br> e linkifica ogni riga in sicurezza.
            return "<br>".join(_linkify_plain_text_to_html(line) for line in value.split("\n"))

        escaped = py_html.escape(value)
        return _linkify_if_available(escaped.replace("\n", "<br>"))

    if bleach is not None:
        cleaned = bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=list(ALLOWED_PROTOCOLS),
            strip=True,
        )
        return _linkify_if_available(_normalize_anchor_hrefs_in_html(cleaned))

    sanitizer = _SimpleHTMLSanitizer(set(ALLOWED_TAGS))
    sanitizer.feed(value)
    sanitizer.close()
    return _linkify_if_available(_normalize_anchor_hrefs_in_html(sanitizer.get_html()))
