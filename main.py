from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_entry = request.form['blog_entry']
        new_post = Blog(blog_title, blog_entry)
        db.session.add(new_post)
        db.session.commit()
    
    posts = Blog.query.filter_by(completed=False).all()
    completed_post = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build A Blog", 
        posts=posts, completed_post=completed_post)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    #post_id = int(request.form['post-id'])
    #post = Blog.query.get(post_id)
    #post.completed = True
    #db.session.add(post)
    #db.session.commit()

    return render_template('newpost.html', title='Build A Blog')

if __name__ == '__main__':
    app.run()