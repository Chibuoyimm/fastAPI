from email.policy import default
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base



class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'keep_existing': True}  # not necessary. had to do wtih filename changes, i think

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False) # server_default sets a default value on the database
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("app.models.User") # this has nothing to do with the database, just with sqlalchemy



class User(Base):
    __tablename__ = "users"
    __table_args__ = {'keep_existing': True} # not necessary. had to do wtih filename changes, i think

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {'keep_existing': True} # not necessary. had to do wtih filename changes, i think

    user_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete=CASCADE), primary_key=True)





