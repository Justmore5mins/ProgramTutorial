from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import requests
from urllib.parse import urlparse

class WebsiteNode(nodes.General, nodes.Element):
    pass

def visit_website_html(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='website-card'))

def depart_website_html(self, node):
    self.body.append('</div>')

class WebsiteDirective(SphinxDirective):
    required_arguments = 1

    def run(self):
        url = self.arguments[0]
        title = url
        favicon = ''

        # Try fetching page title
        try:
            r = requests.get(url, timeout=3)
            if "<title>" in r.text.lower():
                start = r.text.lower().find("<title>") + 7
                end = r.text.lower().find("</title>")
                title = r.text[start:end].strip()
        except Exception:
            pass

        # Favicon (fallback: domain/favicon.ico)
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        favicon = f"{domain}/favicon.ico"

        node = WebsiteNode()
        node['url'] = url
        node['title'] = title
        node['favicon'] = favicon

        return [node]


def html_visit(self, node):
    url = node['url']
    title = node['title']
    favicon = node['favicon']

    self.body.append(f"""
<div class="website-card">
  <div class="website-header">
    <img class="website-icon" src="{favicon}" onerror="this.style.display='none'">
    <a class="website-title" href="{url}" target="_blank">{title}</a>
  </div>
  <div class="website-url">{url}</div>
</div>
    """)


def html_depart(self, node):
    pass


def setup(app):
    app.add_node(
        WebsiteNode,
        html=(html_visit, html_depart),
    )
    app.add_directive("website", WebsiteDirective)

    app.add_css_file("website.css")

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True
    }
