from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.WorkData import WorkData

meta = MetaData()


class Base(DeclarativeBase):
    pass


class Works(Base):
    __tablename__ = 'works'

    id_work = Column(Integer, primary_key=True, index=True)
    list_name = Column(VARCHAR(50))
    work_name = Column(VARCHAR(50))
    # plan = Column(VARCHAR(50))
    fact = Column(VARCHAR(50))
    per_day = Column(VARCHAR(50))
    unit = Column(VARCHAR(50))

    def __init__(self, list_name, work_name, fact, per_day, unit, **kw: Any):
        super().__init__(**kw)
        self.list_name = list_name
        self.work_name = work_name
        self.fact = fact
        self.per_day = per_day
        self.unit = unit


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer)
    user_name = Column(VARCHAR(50))
    first_name = Column(VARCHAR(50))
    second_name = Column(VARCHAR(50))

    def __init__(self, chat_id, user_name, first_name, second_name, **kw: Any):
        super().__init__(**kw)
        self.chat_id = chat_id
        self.user_name = user_name
        self.first_name = first_name
        self.second_name = second_name


engine = create_engine("mysql+mysqlconnector://vladis13570:010203vlad@localhost/bnbc_report_bot", echo=True)
Session = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# def createWork(work):
#     global w

def createWork(work: WorkData):
    with Session(autoflush=False, bind=engine) as db:
        w = Works(work.list_name, work.work_name, work.range_one, work.range_two, work.unit_w)
        db.add(w)
        db.commit()


def createNewUser(user_data):
    with Session(autoflush=False, bind=engine) as db:
        user = db.query(User).filter(User.chat_id == user_data['chat_id']).first()
        if user is None:
            new_user = User(user_data['chat_id'], user_data['user_name'], user_data['first_name'],
                            user_data['second_name'])
            db.add(new_user)
            db.commit()
        else:
            pass


def getWorks():
    with Session(autoflush=False, bind=engine) as db:
        work = db.query(Works).all()
        return work


def get_work_by_id(id_work):
    with Session(autoflush=False, bind=engine) as db:
        work = db.get(Works, id_work)
        return work


def initUser(user_data) -> User:
    return User(user_data['chat_id'], user_data['user_name'], user_data['first_name'], user_data['second_name'])
