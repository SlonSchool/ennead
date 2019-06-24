from typing import Any

import redis
from markdown import Markdown
from markdown.extensions import Extension as MarkdownExtension


class DisallowHTML(MarkdownExtension):
    """Simple extension for Python-Markdown that disallows HTML"""

    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


class DictCache(dict):
    """Dict with .set() method auto-encoding values"""

    def set(self, key: str, value: str, **_: Any) -> None:
        """Set value at key to value.encode('utf-8')"""

        self[key] = value.encode('utf-8')


class CachedMarkdown:
    """Cached markdown renderer"""

    def __init__(self):
        self.engine = Markdown(extensions=['mdx_math', 'fenced_code', DisallowHTML()])
        try:
            self.cache_engine = redis.Redis()
            self.cache_engine.ping()
        except redis.exceptions.ConnectionError:
            self.cache_engine = DictCache()

    def render(self, markdown: str) -> str:
        """Convert Markdown to HTML, or get from cache if already converted"""

        cache_key = f'md:{markdown}'
        html = self.cache_engine.get(cache_key)
        if html is None:
            html = self.engine.convert(markdown)
            # Cache expires in one week
            self.cache_engine.set(cache_key, html, ex=(7 * 24 * 60 * 60))
        return html


MARKDOWN_ENGINE = CachedMarkdown()


def render_markdown(markdown: str) -> str:
    """Render markdown using default renderer"""

    return MARKDOWN_ENGINE.render(markdown)
