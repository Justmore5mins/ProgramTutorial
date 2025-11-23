import os
import sys
sys.path.append(os.path.abspath("./_ext"))

project = 'FRC程式資料庫'
copyright = '2025, Justmore5mins from FRC8569'
author = 'Justmore5mins, FRC8569'

extensions = [
    "website",
    "sphinx_tabs.tabs"
]

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ["_static"]
html_css_files = ["website.css"]

language = 'zh_TW'

html_theme = 'shibuya'
html_static_path = ['_static']
pygments_style = 'fruity'


