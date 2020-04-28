from flask import Flask, render_template
from data import db_session
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'success'
    return render_template('LoginTemplate.html', form=form,
                           title='Login')


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return 'success'
    return render_template('RegisterTemplate.html', form=form,
                           title='Register')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1')
