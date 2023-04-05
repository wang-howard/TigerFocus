import sys
from flask import request, session, render_template, redirect, url_for
from flask_login import login_user, login_required
from . import auth
from .. import db, cas_client
from ..models import User

@auth.route("/login")
def login():
    """
    Redirects to CAS authentification, which returns a ticket to
    validate. If successful, redirects to login prcoessing function.
    """
    try:
        next = request.args.get("next")
        ticket = request.args.get("ticket")
        if not ticket:
            # No ticket, request came from end user, send to CAS login
            cas_login_url = cas_client.get_login_url()
            return redirect(cas_login_url)
        
        print('ticket: %s', ticket)
        print('next: %s', next)
        netid, _, _ = cas_client.verify_ticket(ticket)
        if not netid:
            return render_template("error.html",
                                   message="Failed to verify ticket")
        
        # Login successfully, redirect according to "next" parameter
        login_user(User.query.get(netid))
        session["netid"] = netid
        if User.query.get(netid) is None:
            return render_template("register.html", netid=netid)
        else:
            return redirect(url_for(next))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@auth.route("/newuser", methods=["POST"])
@login_required
def new_user():
    """
    Receives post form from register page and enters new user to
    database, then redirects to user's hub.
    """
    netid = request.form.get("netid")
    first = request.form.get("first")
    last = request.form.get("last")
    user_type = request.form.get("user_type")

    user = User(netid=netid, first_name=first, last_name=last,
                user_type=user_type)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("main.hub"))
