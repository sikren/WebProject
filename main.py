from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from forms.SearchForm import SearchForm
from data.user import User
from api_module import StaticApi

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# Все, что касается login
@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('LoginTemplate.html',
                               message="Wrong login or password",
                               form=form, title='Login')
    return render_template('LoginTemplate.html', form=form,
                           title='Login', message="")


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('RegisterTemplate.html', title='Register',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.username == form.username.data).first():
            return render_template('RegisterTemplate.html', title='Register',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        return redirect('/login')
    return render_template('RegisterTemplate.html', form=form,
                           title='Register')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if request.method == 'POST':
        lonlat = form.lonlat.data
        api = StaticApi([int(ll) for ll in lonlat.split(';')])
        return render_template('Search.html', form=form,
                               map_url=api.get_map())

    return render_template('Search.html', form=form, map_url=None)


@app.route('/')
def main():
    return render_template('MainPage.html')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1', debug=True)
