"""
Creates authentification blueprint to distinguish user auth from normal
view functions.
"""

from flask import Blueprint

auth = Blueprint("auth", __name__, template_folder="app/templates")

from . import views
