from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from app.blog.forms import CommentForm, CreatePostForm, ContactForm
from app.utils.email import send_contract_notification
from app.utils.decorators import admin_only
from app.blog.services import BlogServices
from app.auth.services import AuthServices
from app.utils.security import is_admin

blog_bp = Blueprint("blog", __name__)


@blog_bp.route('/')
def get_all_posts():
    posts = BlogServices.get_all_posts()
    return render_template("index.html", all_posts=posts, current_user=current_user)


# Add a POST method to be able to post comments
@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = BlogServices.get_post_by_id(post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("auth.login"))

        BlogServices.add_comment(
            post=requested_post,
            text=comment_form.comment_text.data,
            author=current_user
        )
    return render_template("post.html", post=requested_post, current_user=current_user, form=comment_form)


@blog_bp.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        BlogServices.create_post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)


@blog_bp.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = BlogServices.get_post_by_id(post_id)

    if post.author != current_user and is_admin(current_user):
        abort(403)

    edit_form = CreatePostForm(post)
    if edit_form.validate_on_submit():
        BlogServices.update_post(
            post,
            title=edit_form.title.data,
            subtitle=edit_form.subtitle.data,
            body=edit_form.body.data,
            img_url=edit_form.img_url.data,
            author=current_user
        )
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, current_user=current_user)


@blog_bp.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post = BlogServices.get_post_by_id(post_id)
    BlogServices.delete_post(post)
    flash("Post deleted successfully!", "success")
    return redirect(url_for('get_all_posts'))


@blog_bp.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@blog_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_contract_notification(form.name.data, form.email.data, form.message.data)
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html", current_user=current_user, form=form)