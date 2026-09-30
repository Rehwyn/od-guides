"""Presentation-only TOC filtering; article headings remain unchanged."""
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class FilterToc(Treeprocessor):
    def run(self, root):
        def filtered(items):
            result = []
            for item in items:
                item['children'] = filtered(item.get('children', []))
                if item['name'] in {'Contents', 'Navigate this guide', 'By Rehwyn'}:
                    result.extend(item['children'])
                else:
                    result.append(item)
            return result
        self.md.toc_tokens = filtered(self.md.toc_tokens)


class GuideTocExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(FilterToc(md), 'guide_toc', 4)


def makeExtension(**kwargs):
    return GuideTocExtension(**kwargs)
