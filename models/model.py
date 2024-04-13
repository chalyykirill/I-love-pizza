import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = 'video'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.Text, nullable=False)
    views = sa.Column(sa.Integer, nullable=False)
    likes = sa.Column(sa.Integer, nullable=False)
    rating = sa.Column(sa.Text)
    category = sa.Column(sa.Text)
    country = sa.Column(sa.Text)
    created_at = sa.created_at = Column(sa.TIMESTAMP, nullable=False)



class Topic(Base):
    __tablename__ = 'topic'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.Text, nullable=False)
    image_id = sa.Column(sa.Integer, sa.ForeignKey('image.id'), nullable=False)
    image = sa.orm.relationship(Image)  # innerjoin=True для JOIN
    questions = sa.orm.relationship('Question')

    users = sa.orm.relationship('User', secondary='topic_user')
    # association
    # users = sa.orm.relationship('TopicUser', back_populates='topic')


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)

    # association
    # topics = sa.orm.relationship('TopicUser', back_populates='user')


class TopicUser(Base):
    __tablename__ = 'topic_user'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    role = sa.Column(sa.Text)

    # association
    # user = sa.orm.relationship(User, back_populates='topics')
    # topic = sa.orm.relationship(Topic, back_populates='users')


class Question(Base):
    __tablename__ = 'question'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    text = sa.Column(sa.Text)
    topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'), nullable=False)
    topic = sa.orm.relationship(Topic)  # innerjoin=True для использования JOIN вместо LEFT JOIN