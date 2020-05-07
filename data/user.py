import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


dialog_to_user = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                  sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id')),
                                  sqlalchemy.Column('dialog_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('dialog.id')),
                                  )


class User(SqlAlchemyBase):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    dialogs = relationship('Dialog', secondary=dialog_to_user, back_populates='users')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> id={self.id}, username={self.username}'