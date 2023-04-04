"""
Error handler file for Flask app.
"""

from flask import render_template
from . import bp

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("placeholder"), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template("placeholder"), 500