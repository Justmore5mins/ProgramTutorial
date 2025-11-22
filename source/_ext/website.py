from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import requests
from urllib.parse import urlparse

class WebsiteNode(nodes.General, nodes.Element):
    pass

class WebsiteDirective(SphinxDirective):
    required_arguments = 1      # URL
    option_spec = {
        'title': lambda x: x,   # custom title
    }

    def run(self):
        url = self.arguments[0]

        # If user gives :title:, use it
        if 'title' in self.options:
            title = self.options['title']
        else:
            title = url
            # Auto-fetch page title
            try:
                r = requests.get(url, timeout=3)
                html_lower = r.text.lower()
                if "<title>" in html_lower:
                    start = html_lower.find("<title>") + 7
                    end = html_lower.find("</title>")
                    title = r.text[start:end].strip()
            except Exception:
                pass

        # Favicon
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
