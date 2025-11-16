# -- Path setup --------------------------------------------------------------

import os
import sys
from pathlib import Path

# If your modules are in scripts or elsewhere
# sys.path.insert(0, os.path.abspath('../scripts'))

# -- Project information -----------------------------------------------------

project = 'UK Coast Walk Tracker'
author = 'Your Name'
release = '1.0'
copyright = "© 2025 Mohana Das"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",          # for Markdown support
]

# Allow MyST to parse standard Markdown with links
myst_enable_extensions = [
    "linkify",
]

# Recognize .md files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# Templates and static paths
templates_path = ['_templates']
html_static_path = ['_static']

# Theme
html_theme = 'sphinx_rtd_theme'

# Sidebar maxdepth
html_theme_options = {
    'navigation_depth': 2,  # Controls levels of sidebar
}
