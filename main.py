from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bruh@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'j3l230H19'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.completed = False
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    entries = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('Logged in!')
            return redirect('/')
        else:
            flash('User pasword incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        if email == '':
            flash('Please enter a valid email address')
            return redirect('/register')
        if password == "":
            flash('Please enter a password')
            return redirect('/register')
        if verify == "":
            flash('Please verify your password')
            return redirect('/register')
        
        if not existing_user and password == verify:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        elif not existing_user and password != verify:
            flash("Passwords don't match!")
            return redirect('/register')
        elif existing_user:
            flash('Duplicate User!')
            return redirect('/register')


    return render_template('register.html')

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():
    owner = User.query.filter_by(email=session['email']).first()
    
    if request.args.get("id"):
        new_post = Blog.query.filter_by(id=request.args.get("id")).first()
        return render_template("newentry.html", new_post=new_post)
    
    
    posts = Blog.query.filter_by(completed=False, owner=owner).all()
    completed_post = Blog.query.filter_by(completed=True).all()
    return render_template('blog.html',title="Build A Blog", 
        posts=posts, completed_post=completed_post)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''
    owner = User.query.filter_by(email=session['email']).first()
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
            new_post = Blog(blog_title, blog_entry, owner)
            db.session.add(new_post)
            db.session.commit()
            new_post.id
            return redirect('/?id=' + str(new_post.id))

    return render_template('newpost.html', title='Build A Blog', title_error=title_error, body_error=body_error)

if __name__ == '__main__':
    app.run()