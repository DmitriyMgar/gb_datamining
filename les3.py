from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship

Base = declarative_base()

tag_post = Table('tag_post', Base.metadata,
                 Column('post_id', Integer, ForeignKey('post.id')),
                 Column('tag_id', Integer, ForeignKey('tag.id')),
                 )


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    writer_id = Column(String, ForeignKey('writer.id'))
    writer = relationship('Writer', back_populates='post')
    tag = relationship('Tag', secondary=tag_post, back_populates='post')


class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    post = relationship('Post', back_populates='writer')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=False, nullable=False)
    url = Column(String, unique=False, nullable=False)
    post = relationship('Post', secondary=tag_post, back_populates='tag')


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import Session

    engine = create_engine('sqlite:///gb_blog.db')
    Base.metadata.create_all(engine)
    session_db = sessionmaker(bind=engine)

    session = session_db()

    try:
        session.add()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


    print(1)
