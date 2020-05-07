from flask import Flask, render_template, request, session, redirect
from data import db_session, user, dialog
from forms.LoginForm import LoginForm
import datetime

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
    pass


# костыль чтобы самому себе сессию на что надо ставить
@app.route('/set_session', methods=['GET'])
def set_session():
    all_args = request.args.lists()
    session['user_id'] = list(all_args)[0][1][0]
    return 'smh'


@app.route('/add_dialog', methods=['GET'])
def add_dialog():
    second_user_id = request.args.get('second_user')
    new_dialog = dialog.Dialog()

    ses = db_session.create_session()
    user_obj = ses.query(user.User).filter(user.User.id == int(session['user_id'])).first()
    second_user_obj = ses.query(user.User).filter(user.User.id == second_user_id).first()
    new_dialog.users.append(user_obj)
    new_dialog.users.append(second_user_obj)
    ses.add(new_dialog)
    ses.commit()
    return 'nice'


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        ses = db_session.create_session()

        dialog_id = int(request.args.get('id'))
        text = request.form.get('text').strip()
        timestamp = datetime.datetime.today()
        sender = int(session['user_id'])

        message = dialog.Message()
        message.text = text
        message.timestamp = timestamp
        message.user_id = sender
        message.dialog_id = dialog_id

        ses.add(message)
        ses.commit()

    if 'user_id' in session:
        user_id = int(session['user_id'])
        ses = db_session.create_session()
        user_object = ses.query(user.User).filter(user.User.id == user_id).first()
        dialogs_render = []

        selected_dialog_id = request.args.get('id')
        if selected_dialog_id is None:
            return redirect(f'/messages?id={user_object.dialogs[0].id}')

        for d in user_object.dialogs:
            other_user = list(filter(lambda x: x.id != user_object.id, d.users))[0]

            last_message = sorted(d.messages, key=lambda x: x.id)[-1]

            d_render = {'id': str(d.id), 'selected': (selected_dialog_id == d.id), 'name': other_user.username,
                        'last_message': last_message.text}
            dialogs_render.append(d_render)
        selected_dialog = list(filter(lambda x: x.id == int(selected_dialog_id), user_object.dialogs))[0]
        messages_render = []
        for m in selected_dialog.messages:
            sender = ses.query(user.User).filter(user.User.id == m.user_id).first()
            m_render = {'you': (m.user_id == user_id), 'from': sender.username, 'text': m.text, 'time': m.timestamp}
            messages_render.append(m_render)

        return render_template('MessagesTemplate.html', title='Чаты', dialogs=dialogs_render, messages=messages_render)
    else:
        return redirect('/login')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(port=8080, host='127.0.0.1')
