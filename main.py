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
    if request.args.get("id"):
        new_post = Blog.query.filter_by(id=request.args.get("id")).first()
        return render_template("newentry.html", new_post=new_post)
    
    
    posts = Blog.query.filter_by(completed=False).all()
    completed_post = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build A Blog", 
        posts=posts, completed_post=completed_post)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''
    if request.method == 'POST':
        title = request.form['blog_title']
        body = request.form['blog_entry']
        if not title:
            title_error = "Please enter a title"

        if not body:
            body_error = "Please add an entry"

        if not title_error and not body_error:
            blog_title = request.form['blog_title']
            blog_entry = request.form['blog_entry']
            new_post = Blog(blog_title, blog_entry)
            db.session.add(new_post)
            db.session.commit()
            new_post.id
            return redirect('/?id=' + str(new_post.id))

    return render_template('newpost.html', title='Build A Blog', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()