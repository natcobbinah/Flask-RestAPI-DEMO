from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.db import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    def get_user_id(self):
        return self.id
