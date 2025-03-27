from flask import Blueprint, render_template, session, url_for, redirect, current_app

bp_google_auth = Blueprint("google_login", __name__, template_folder="templates")


@bp_google_auth.route("/home")
def homepage():
    user = session.get("user")
    return render_template("home.html", user=user)


@bp_google_auth.route("/login")
def login():
    redirect_uri = url_for("google_login.auth", _external=True)
    return current_app.config["oauth"].google.authorize_redirect(redirect_uri)
    # return oauth.google.authorize_redirect(redirect_uri)


@bp_google_auth.route("/auth")
def auth():
    token = current_app.config["oauth"].google.authorize_access_token()
    session["user"] = token["userinfo"]
    return redirect("/home")


@bp_google_auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/home")
