from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, ContactForm
from model import User
from extensions import db
from utils import send_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        result1 = User.query
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("blog.get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('blog.get_all_posts'))

    return render_template("login.html", form=form, current_user=current_user)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog.get_all_posts'))


@auth_bp.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@auth_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(form.name.data, form.email.data, form.message.data)
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", current_user=current_user, form=form)
