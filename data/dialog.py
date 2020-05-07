import sqlalchemy
from .user import dialog_to_user
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Dialog(SqlAlchemyBase):
    __tablename__ = 'dialog'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    users = relationship('User', secondary=dialog_to_user, back_populates='dialogs')
    messages = relationship('Message')


class Message(SqlAlchemyBase):
    __tablename__ = 'message'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    dialog_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('dialog.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
