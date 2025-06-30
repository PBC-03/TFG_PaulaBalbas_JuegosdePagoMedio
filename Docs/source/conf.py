# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  #Se va al directorio raíz (dos niveles hacia arriba). Así puede leer los .py

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'TFG Paula Balbás Corbacho - Juegos de pago medio' #sale arriba a la izquierda en la doc de sphinx_rtd_theme
copyright = '2025, Paula Balbás Corbacho' #En la parte inferior de la doc
author = 'Paula Balbás Corbacho'

# The full version, including alpha/beta/rc tags
release = '1-07-2025'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc'] #Para que se genere la documentación de los módulos Python automáticamente

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme' #tema que importamos
#html_theme = 'sphinx_book_theme'
#html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

#Generar la doc: 
# .\make.bat html (esto lo ejecutamos desde la carpeta Docs)
# start .\build\html\index.html (para abrir la doc en el navegador)