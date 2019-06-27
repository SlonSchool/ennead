"""Module with properly configured Markdown renderer"""

from typing import Any

import redis
from markdown import Markdown
from markdown.util import etree as ElementTree
from markdown.extensions import Extension as MarkdownExtension
from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor


class DisallowHTML(MarkdownExtension):
    """Simple extension for Python-Markdown that disallows HTML"""

    def extendMarkdown(self, md: Markdown) -> None:
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


class BetterImages(ImageInlineProcessor):
    """Return a clickable & zoomable image from the given match with additional classes"""

    def handleMatch(self, m, data):
        image, m_start, index = super().handleMatch(m, data)
        image.set('class', 'markdown-image img-thumbnail')
        elem = ElementTree.Element('a')
        elem.set('href', image.get('src'))
        elem.set('target', '_blank')
        elem.set('data-lity', '')
        elem.append(image)
        return elem, m_start, index


class DictCache(dict):
    """Dict with .set() method auto-encoding values"""

    def set(self, key: str, value: str, **_: Any) -> None:
        """Set value at key to value.encode('utf-8')"""

        self[key] = value.encode('utf-8')


class CachedMarkdown:
    """Cached markdown renderer"""

    def __init__(self):
        self.engine = Markdown(
            extensions=['mdx_math', 'fenced_code', 'nl2br', DisallowHTML()]
        )
        self.engine.inlinePatterns.register(
            BetterImages(IMAGE_LINK_RE, self.engine),
            'image_link',
            150
        )
        try:
            self.cache_engine = redis.Redis()
            self.cache_engine.ping()
        except redis.exceptions.ConnectionError:
            self.cache_engine = DictCache()

    def render(self, markdown: str) -> str:
        """Convert Markdown to HTML, or get from cache if already converted"""

        cache_key = f'md:{markdown}'
        try:
            html = self.cache_engine.get(cache_key)
        except redis.exceptions.RedisError:
            html = None
        if html is None:
            html = self.engine.convert(markdown)
            # Cache expires in one week
            try:
                self.cache_engine.set(cache_key, html, ex=(7 * 24 * 60 * 60))
            except redis.exceptions.RedisError:
                pass
        return html


MARKDOWN_ENGINE = CachedMarkdown()


def render_markdown(markdown: str) -> str:
    """Render markdown using default renderer"""

    return MARKDOWN_ENGINE.render(markdown)
