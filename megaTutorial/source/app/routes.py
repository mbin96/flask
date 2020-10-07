from flask import render_template, flash, redirect, url_for,request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
@login_required #이러달면 로그인을 해야만 볼수 있게 해줌(/login?next=/index)
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username':'John'},
            'body': 'Beautiful day in Portland'
        },
        {
            'author':{'username': 'Susan'},
            'body': 'The Avengers movie was so cool'
        }

    ]
    return render_template('index.html', title = 'home', posts=posts)




@app.route('/login', methods = ['GET', 'POST'])
def login():
    # already login user
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        # 일치하는 user을 db에서 쿼리
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        #어규멘트로 들어온 nexturl 파싱
        next_page = request.args.get('next')
        #어규멘트가 없거나 netloc가 있는 (즉 풀도메인)인경우 경우 index 페이지로
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
