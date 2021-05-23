from flask import Blueprint, render_template, session, g, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from apps.db import get_db

bp = Blueprint('views', __name__)


@bp.route('/')
def index():
    # 启动页
    return render_template('index.html')


@bp.before_app_request
def load():
    # 加载
    userid = session.get('userid')

    if userid is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE userid = ?", (userid,)).fetchone()


@bp.route('/home', methods=['GET'])
def home():
    # 首页
    if request.method == 'GET':
        return render_template('index.html')
    return redirect('/')


@bp.route('/head', methods=['GET'])
def head():
    # 页头
    if request.method == 'GET':
        username = session.get('username')
        return render_template('head.html', username=username)


@bp.route('/left', methods=['GET'])
def left():
    # 左侧
    if request.method == 'GET':
        # username = session.get('username')
        return render_template('left.html')


@bp.route('/main/', methods=['GET', 'POST'])
def main():
    # 主体
    if request.method == 'GET':
        db = get_db()
        total_goods = db.execute(
            "SELECT * FROM good"
        ).fetchall()

        num = 2
        total = len(total_goods)
        page = int(request.args.get('page', 1))
        maxpage = total//num + 1
        goods = total_goods[num*(page-1):num*page]

        return render_template('main.html', goods=goods, page=page, maxpage=maxpage, total=total)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        db = get_db()

        msg, flag = None, 0
        if not all([username, password, repassword]):
            msg, flag = '* 请填写完整信息', 1
        elif len(username) > 16:
            msg, flag = '* 用户名太长', 1
        elif (
                db.execute("SELECT userid FROM user WHERE username = ?", (username,)).fetchone()
                is not None
        ):
            msg, flag = '* 用户名已注册', 1
        elif password != repassword:
            msg, flag = '* 两次密码不一致', 1
        elif len(password) < 6 or len(password) > 16:
            msg, flag = '* 密码长度必须在6和16之间', 1
        if flag:
            return render_template('register.html', msg=msg)
        else:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for('views.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        msg = None
        if not all([username, password]):
            msg = '* 请填写好完整的信息'
            return render_template('login.html', msg=msg)

        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            msg = "* 错误的用户名或密码"
        elif not check_password_hash(user["password"], password):
            msg = "* 错误的用户名或密码"
        if msg:
            return render_template('login.html', msg=msg)
        else:
            session.clear()
            session['userid'] = user['userid']
            session['username'] = user['username']
            return redirect(url_for('views.home'))


@bp.route('/logout', methods=['GET'])
def logout():
    # 注销
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('user.login'))
