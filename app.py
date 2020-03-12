# Web app that works with a database and allows you to read and write
# to it.
# Created following Youtube Tutorial https://www.youtube.com/watch?v=3mwFC4SHY-Y&t=3913s
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #Constructor
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(application)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    data_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post '+ str(self.id)

all_posts = [
    {
        'title': 'Post 1',
        'content': 'Content of post 1 here',
        'author': 'Pepe'
    },
    {
        'title': 'Post 2',
        'content': 'Content of post 2 here',
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.data_posted.desc()).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/home/<string:name>')
def method(name):
    return "Pepe el gorila tambien conocido como "+ name
@app.route('/onlyget', methods=['GET'])
def get_only():
    return 'you can only get this webpage 2'

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new', methods=['GET', 'POST'])
def newest_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')





if __name__ == "__main__":
    application.run(debug=True)
