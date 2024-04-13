import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from database.connector import engine, get_session, get_connection, execute_query

BaseModel = declarative_base()

class Video(BaseModel):
    __tablename__ = 'Video'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True, unique=True, autoincrement=True)
    guid = sa.Column(sa.String, nullable=False, index=True, unique=True)
    video_url = sa.Column(sa.Text, nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text)
    duration = sa.Column(sa.Integer, nullable=False)
    hits = sa.Column(sa.Integer, nullable=False)
    likes = sa.Column(sa.Integer, nullable=False)
    pg_rating = sa.Column(sa.Text)
    category_name = sa.Column(sa.Text)
    allowed_territories = sa.Column(MutableDict.as_mutable(JSONB))
    disallowed_territories = sa.Column(MutableDict.as_mutable(JSONB))
    created_at = sa.Column(sa.TIMESTAMP, nullable=False)
    updated_at = sa.Column(sa.TIMESTAMP, nullable=False)

    autor_id = sa.Column(sa.Integer, sa.ForeignKey('Author.id'), nullable=False)
    author = sa.orm.relationship('Author', back_populates='videos')
    category_id = sa.Column(sa.Integer, sa.ForeignKey('Category.id'), nullable=False)
    category = sa.orm.relationship('Category', back_populates='videos')

class Author(BaseModel):
    __tablename__ = 'Author'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True, unique=True)
    name = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text)
    subscribers = sa.Column(sa.Integer)
    created_at = sa.Column(sa.TIMESTAMP)
    updated_at = sa.Column(sa.TIMESTAMP)
    site_url = sa.Column(sa.Text)

    videos = sa.orm.relationship('Video', back_populates='author')

class Category(BaseModel):
    __tablename__ = 'Category'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True, unique=True)
    name = sa.Column(sa.Text, nullable=False)
    category_url = sa.Column(sa.Text)

    videos = sa.orm.relationship('Video', back_populates='category')

class Comment(BaseModel):
    __tablename__ = 'Comment'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True, unique=True)
    video_id = sa.Column(sa.Integer, sa.ForeignKey('Video.id'), nullable=False)
    video = sa.orm.relationship('Video', back_populates='comments')
    root_id = sa.Column(sa.Integer, sa.ForeignKey('Comment.id'), default=None)
    answers = sa.orm.relationship('Comment', back_populates='root')
    text = sa.Column(sa.Text)
    tone = sa.Column(sa.String)
    likes = sa.Column(sa.Integer)
    dislikes = sa.Column(sa.Integer)

# Create tables,engine is async

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
    loop.close()


# class Topic(Base):
#     __tablename__ = 'topic'

#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     title = sa.Column(sa.Text, nullable=False)
#     image_id = sa.Column(sa.Integer, sa.ForeignKey('image.id'), nullable=False)
#     image = sa.orm.relationship(Image)  # innerjoin=True для JOIN
#     questions = sa.orm.relationship('Question')

#     users = sa.orm.relationship('User', secondary='topic_user')
#     # association
#     # users = sa.orm.relationship('TopicUser', back_populates='topic')


# class User(Base):
#     __tablename__ = 'user'

#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     name = sa.Column(sa.Text, nullable=False)

#     # association
#     # topics = sa.orm.relationship('TopicUser', back_populates='user')


# class TopicUser(Base):
#     __tablename__ = 'topic_user'

#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'))
#     user_id = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
#     role = sa.Column(sa.Text)

#     # association
#     # user = sa.orm.relationship(User, back_populates='topics')
#     # topic = sa.orm.relationship(Topic, back_populates='users')


# class Question(Base):
#     __tablename__ = 'question'

#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
#     text = sa.Column(sa.Text)
#     topic_id = sa.Column(sa.Integer, sa.ForeignKey('topic.id'), nullable=False)
#     topic = sa.orm.relationship(Topic)  # innerjoin=True для использования JOIN вместо LEFT JOIN
