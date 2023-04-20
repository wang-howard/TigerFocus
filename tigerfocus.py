"""
Application file for TigerFocus. Use this python for running the
application either using "flask run" with the FLASK_APP env variable set
or "python tigerfocus.py" in terminal.

SET THESE ENVIRONMENT VARIABLES ON STARTUP:
export FLASK_APP=tigerfocus.py
export DB_URI=postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq
export SEC_KEY=tigerFocus098098
export SERVICE_URL=http://localhost:5553/login?next=main.hub
"""

from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Course, Assignment

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Course=Course, Assignment=Assignment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5553", debug=True)