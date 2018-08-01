from flask import Blueprint,render_template,url_for,flash,redirect,request
from Blog import bcrypt,db
from Blog.users.forms import RegisterForm,LoginForm
from Blog.models import User
from flask_login import login_user, current_user, logout_user, login_required

users=Blueprint('users',__name__)


@users.route('/register/',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        pw_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data ,email=form.email.data,password=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form)


@users.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('users.home'))
    return render_template('login.html',form=form)

@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/home/')
def home():
    return render_template('home.html')
