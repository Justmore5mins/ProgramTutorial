# AutoGlossary.py
from docutils import nodes
import re
import os

def setup(app):
    app.connect('doctree-resolved', process_autoglossary)
    app.add_config_value('autoglossary_file', 'LinkedDocuments/SpecificNouns.rst', 'env')
    return {'version': '1.0', 'parallel_read_safe': True, 'parallel_write_safe': True}

aliases = {}

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

def process_autoglossary(app, doctree, fromdocname):
    src_dir = app.srcdir
    glossary_path = os.path.join(src_dir, app.config.autoglossary_file)
    if not os.path.exists(glossary_path):
        app.warn(f"AutoGlossary: file not found: {glossary_path}")
        return

    # Step 1: 解析 glossary
    with open(glossary_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if set(stripped) == set("+") and len(stripped) >= 4:
            main_title_line = lines[i - 1].strip()
            title_parts = [x.strip() for x in main_title_line.split("/")]
            main_term = title_parts[0]
            anchor = f"auto-term-{main_term.replace(' ', '-')}"
            for part in title_parts:
                aliases[normalize(part)] = (main_term, anchor)

    # Step 2: 替換正文文字 → 參考連結
    for node in doctree.traverse(nodes.Text):
        parent = node.parent
        if isinstance(parent, nodes.reference):
            continue

        text = node.astext()
        new_nodes = []
        last_index = 0

        for alias_norm, (main_term, anchor) in aliases.items():
            pattern = re.compile(r'\b{}\b'.format(re.escape(alias_norm)), re.IGNORECASE)
            for m in pattern.finditer(text):
                start, end = m.span()
                if start > last_index:
                    new_nodes.append(nodes.Text(text[last_index:start]))
                ref_node = nodes.reference(text=m.group(0), refuri=f"#{anchor}")
                new_nodes.append(ref_node)
                last_index = end
        if new_nodes:
            if last_index < len(text):
                new_nodes.append(nodes.Text(text[last_index:]))
            parent.replace(node, new_nodes)
