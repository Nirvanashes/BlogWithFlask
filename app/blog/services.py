from datetime import date
from app.blog.models import BlogPost, Comment
from app.extensions import db


class BlogServices:
    @staticmethod
    def get_all_posts():
        return db.session.execute(db.select(BlogPost)).scalars().all()

    @staticmethod
    def get_post_by_id(post_id: int):
        return db.get_or_404(BlogPost, post_id)

    @staticmethod
    def create_post(title, subtitle, body, img_url, author):
        new_post = BlogPost(
            title=title,
            subtitle=subtitle,
            body=body,
            img_url=img_url,
            author=author,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def update_post(post: BlogPost, title, subtitle, body, img_url, author):
        post.title = title
        post.subtitle = subtitle
        post.body = body
        post.img_url = img_url
        post.author = author
        db.session.commit()
        return post

    @staticmethod
    def delete_post(post):
        db.session.delete(post)
        db.session.commit()

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
