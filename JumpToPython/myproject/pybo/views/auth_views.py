from flask import Blueprint, url_for, render_template, flash, request, session, g
## generate_password_hash 비밀번호 암호화
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

import functools
from ..db import db
from pybo.forms import UserCreateForm , UserLoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    cursor = db.cursor()
    if request.method == 'POST' and form.validate_on_submit():
        sql = "select * from user where username='{}'".format(form.username.data)
        cursor.execute(sql)
        user = cursor.fetchone()
        if not user:
            sql = "insert into user (username, password, email) values ('{}','{}','{}');".format(form.username.data, generate_password_hash(form.password1.data), form.email.data)
            cursor.execute(sql)
            db.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    ## forms.py에서 폼 불러오긴
    form = UserLoginForm()
    cursor = db.cursor()
    ## db에 존재하는 사용자 조회 및 인증처리
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        sql = "select * from user where username='{}'".format(form.username.data)
        cursor.execute(sql)
        user = cursor.fetchone()
        if not user:
            error = "존재하지 않는 사용자입니다."
        ## 비밀번호 해쉬값 decrypt  (디비조회한 해쉬값 , 실제 폼에 적은 비밀번호)
        elif not check_password_hash(user['password'], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        ## 로그인 성공시 세션에 id와 이름 등록 후 메인으로 리다이렉트
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('main.index'))
        flash(error)

    ## 로그인 페이지 뿌려줘
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = {'user_id': session.get('user_id'), 'username': session['username']}

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))