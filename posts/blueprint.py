from flask import Blueprint, render_template, redirect, url_for

pos = Blueprint('pos', __name__, template_folder='templates')
from flask import request
from models import Post, Tag
from .forms import PostForm
from app import db


@pos.route("/create", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except Exception:
            print Exception
        return redirect(url_for('pos.index'))
    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@pos.route('/')
def index():
    q = request.args.get('q', '')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=4)

    return render_template('posts/index.html', posts=posts, pages=pages)


# edit
@pos.route("/<slug>/edit/", methods=["POST", "GET"])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == "POST":
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('pos.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)



@pos.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@pos.route("/tag/<slug>")
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts.all()
    return render_template('/posts/tag_detail.html', tag=tag, posts=posts)
