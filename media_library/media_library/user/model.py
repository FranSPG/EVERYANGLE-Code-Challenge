from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from media_library.db import Base
from . import hashing


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(255), unique=True)
    password = Column(String(255))

    media = relationship("Media", back_populates="user", uselist=False)

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = hashing.get_password_hash(password)

    def check_password(self, password):
        return hashing.verify_password(self.password, password)

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }
