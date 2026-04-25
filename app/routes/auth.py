from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar o sistema.", "warning")
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@auth_bp.get("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.post("/register")
def register_post():
    service = AuthService()
    form_data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "password": request.form.get("password", ""),
        "whatsapp": request.form.get("whatsapp", "").strip(),
    }
    success, message = service.register_user(form_data)

    if not success:
        flash(message, "danger")
        return render_template("auth/register.html", form_data=form_data), 400

    flash("Conta criada com sucesso. Faça login para continuar.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.get("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.post("/login")
def login_post():
    service = AuthService()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    authenticated_user = service.authenticate(email=email, password=password)

    if authenticated_user is None:
        flash("E-mail ou senha inválidos.", "danger")
        return render_template("auth/login.html", form_data={"email": email}), 401

    session.clear()
    session["user_id"] = authenticated_user.id
    session["user_name"] = authenticated_user.name

    flash("Login realizado com sucesso.", "success")
    return redirect(url_for("core.home"))


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("auth.login"))
