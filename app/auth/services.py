from app.blog.models import Comment
from app.extensions import db


class AuthServices:

    @staticmethod
    def add_comment(post, text, author):
        new_comment = Comment(
            text=text,
            comment_author=author,
            parent_post=post
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
