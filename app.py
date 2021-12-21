from _init_ import app,db,login_manager
from flask import render_template, request,redirect
from db import DB
from verify import Verify
from flask_login import login_user, login_required,logout_user
from login_form import LoginForm
from register_form import RegisterForm
from data_manage import data_manage_bp
from annotation import annotation_bp
from task_manage import task_manage_bp
from group_manage import group_manage_bp
from download_manage import download_manage_bp
from table_page_manage import table_page_manage_bp

app.register_blueprint(data_manage_bp, url_prefix='/data_manage')
app.register_blueprint(annotation_bp, url_prefix='/annotation')
app.register_blueprint(task_manage_bp, url_prefix='/task_manage')
app.register_blueprint(group_manage_bp, url_prefix='/group_manage')
app.register_blueprint(download_manage_bp, url_prefix='/download_manage')
app.register_blueprint(table_page_manage_bp, url_prefix='/table_page_manage')
app.jinja_env.auto_reload = True

d = DB()
v = Verify()


@login_manager.user_loader
def load_user(username):
    if d.query_by_username(username) is not None:
        user = d.query_by_username(username)
    else:
        user = d.query_by_email(username)
    return user


@app.route('/main')
@login_required
def main_page():
    return render_template('index.html')


@app.route('/data')
@login_required
def data_page():
    return render_template('data.html')


@app.route('/task')
@login_required
def task_page():
    return render_template('task.html')


@app.route('/group')
@login_required
def group_page():
    return render_template('group.html')


@app.route('/download')
@login_required
def download_page():
    return render_template('download.html')


@app.route('/table_page')
@login_required
def table_page():
    return render_template('table_page.html')


@app.route('/')
def main():
    # 不存在则返回None
    # d.new_password('11', '11', '123')
    # v.write_code('zhaox917@163.com')
    # x = v.write_code('zhaox917@163.com')
    # x = v.verification('zhaox917@163.com', '252819')
    # return x
    form = LoginForm()
    return render_template('login_page.html', form=form)


@app.route('/success')
@login_required
def index():
    return render_template('success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        x = d.check_login(username=form.username.data, email=form.username.data, password=form.password.data)
        print(x)
        if x == 1:
            if d.query_by_username(form.username.data) != None:
                user = d.query_by_username(form.username.data)
            else:
                user = d.query_by_email(form.username.data)
            login_user(user)
            return redirect('/main')
        if x == -1:
            return render_template('login_page.html', form=form, inf='用户名（邮箱）不存在！')
        if x == 0:
            return render_template('login_page.html', form=form, inf='用户名（邮箱）和密码不匹配！')

    return render_template('login_page.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    form = LoginForm()
    return render_template('login_page.html', form=form)

@app.route('/register_page')
def register_page():
    form = RegisterForm()
    return render_template('register_page.html', form=form)

@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    username = form.username.data
    email = form.email.data
    password = form.password.data
    en_password = form.en_password.data
    code = form.code.data

    if username == '':
        return render_template('register_page.html', inf='用户名不能为空！')
    elif email == '':
        return render_template('register_page.html', inf='邮箱不能为空！')
    elif password == '':
        return render_template('register_page.html', inf='密码不能为空！')
    elif en_password == '':
        return render_template('register_page.html', inf='确认密码不能为空！')
    elif code == '':
        return render_template('register_page.html', inf='验证码不能为空！')
    elif d.query_by_username(username) is not None:
        return render_template('register_page.html', inf='用户名已存在！')
    elif d.query_by_email(email) is not None:
        return render_template('register_page.html', inf='该邮箱已注册！')
    elif password != en_password:
        return render_template('register_page.html', inf='两次密码不一致！')
    else:
        x = v.verification(email, code)
        if x == '验证成功':
            d.add_user(username, email, password, '用户')
            return render_template('register_success.html', username=username)
        else:
            return render_template('register_page.html', inf=x)


@app.route('/send_code', methods=['POST'])
def send_code():
    email = request.form.get('email')
    return v.write_code(email)




if __name__ == '__main__':
    app.run(debug=True)
