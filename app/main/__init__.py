"""
Creates Flask blueprint to be used by views.py to direct routes. Views
and errors must be imported after bp is initialized due to circular
dependencies.
"""

from flask import Blueprint

bp = Blueprint("main", __name__)

from . import views_hub, views_nav, views_public, errors
