import sqlalchemy as sa
from database.connector import engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
BaseModel = declarative_base()

class Video(BaseModel):
    __tablename__ = 'Video'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False, index=True, unique=True, autoincrement=True)
    guid = sa.Column(sa.String, nullable=False, index=True, unique=True)
    video_url = sa.Column(sa.Text, nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    description = sa.Column(sa.Text)
    description_tone = sa.Column(sa.String)
    duration = sa.Column(sa.Integer, nullable=False)
    hits = sa.Column(sa.Integer, nullable=False)
    likes = sa.Column(sa.Integer)
    dislikes = sa.Column(sa.Integer)
    pg_rating = sa.Column(sa.Integer)
    category_name = sa.Column(sa.Text)
    allowed_territories = sa.Column(MutableDict.as_mutable(JSONB))
    disallowed_territories = sa.Column(MutableDict.as_mutable(JSONB))
    created_at = sa.Column(sa.TIMESTAMP, nullable=False)
    updated_at = sa.Column(sa.TIMESTAMP, nullable=False)

    autor_id = sa.Column(sa.Integer, sa.ForeignKey('Author.id'), nullable=False)
    author = sa.orm.relationship('Author', back_populates='videos')
    category_id = sa.Column(sa.Integer, sa.ForeignKey('Category.id'), nullable=False)
    category = sa.orm.relationship('Category', back_populates='videos')
    comments = sa.orm.relationship('Comment', back_populates='video')

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

    id = sa.Column(sa.BigInteger, primary_key=True, nullable=False, index=True, unique=True)
    video_id = sa.Column(sa.Text, sa.ForeignKey('Video.guid'), nullable=False)
    video = sa.orm.relationship('Video', back_populates='comments')
    root_id = sa.Column(sa.Integer, sa.ForeignKey('Comment.id'), default=None)
    answers = sa.orm.relationship('Comment', back_populates='root')
    root = sa.orm.relationship('Comment', back_populates='answers', remote_side=[id])
    text = sa.Column(sa.Text)
    tone = sa.Column(sa.String)
    likes = sa.Column(sa.Integer)
    dislikes = sa.Column(sa.Integer)

# Create tables, engine is async

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
    loop.close()