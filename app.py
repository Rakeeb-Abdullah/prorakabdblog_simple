from datetime import datetime
from flask import Flask, render_template, request, redirect,make_response
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'mysecret'

admin = Admin(app, name='app',url='/admin_interface')
login = LoginManager(app)

class User(db.Model ,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(UserView(BlogPost, db.session))
admin.add_view(UserView(User, db.session))
'''
all_posts = [
    {
        'title' : 'Post-1',
        'content' : 'lallalalallalal',
        'author' : 'Rakeeb Abdullah',
    },
    {
        'title' : 'Post-2',
        'content' : 'lallalalallalal',
    },
]
'''


@app.route('/')
def hello():
   return render_template('index.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    '''
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)
    '''
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)

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
       return redirect('/posts/read_more/'+str(post.id))
    
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        author = request.form['author']
        new_post = BlogPost(
            title=post_title, content=post_content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('new_post.html', posts=all_posts)
@app.route('/posts/read_more/<int:id>')
def read_more(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('read_more.html',post=post)


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).all():
            user = User.query.filter_by(username=username).all()
            if user[0].password == password:
                current_userr = user[0]
                login_user(current_userr)
                return render_template('loggedin.html')
            else:
                return render_template('login_fail.html')
        else:
            return render_template('login_fail.html')
    else:
        return render_template('admin_login.html')

@app.route('/logout')
def method_name():
   logout_user()
   return render_template('log_out.html')

if __name__ == '__main__':
    app.run(debug=True)
