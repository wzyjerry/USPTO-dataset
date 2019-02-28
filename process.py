from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.types import DateTime
from sqlalchemy.interfaces import PoolListener

from sqlalchemy import func

DB_URL = 'sqlite:///patent.db'

class MyListener(PoolListener):
    def connect(self, dbapi_con, con_record):
        dbapi_con.execute("PRAGMA temp_store = 2")

engine = create_engine(DB_URL, listeners=[MyListener()])

def load_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
session = load_session()
Base = declarative_base()

class Patent(Base):
    __tablename__ = 'patent'
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True)
    category = Column(String)
    pub_number = Column(String)
    app_number = Column(String)
    pub_date = Column(DateTime)
    title = Column(String)
    abstract = Column(String)
    description = Column(String)
    claims = Column(String)

    def to_dict(self):
        d = {}
        d['id'] = self.id
        d['category'] = self.category
        d['pub_date'] = self.pub_date
        d['title'] = self.title
        d['abstract'] = self.abstract
        d['description'] = self.description
        d['claims'] = self.claims
        d['cited_patents'] = [c.cited_pat for c in self.cited_patents]
        return d

    def __repr__(self):
        return "<Patent(id='%s', category='%s', pub_number='%s', app_number='%s',\
                        pub_date='%s', title='%s', abstract='%s', description='%s',\
                        claims='%s', cited_patents='%s')>" %(self.id, self.category,
                        self.pub_number, self.app_number, str(self.pub_date), self.title,
                        self.abstract, self.description, self.claims, self.cited_patents)

class Citation(Base):
    __tablename__ = 'citation'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    citing_pat = Column(String, ForeignKey(Patent.id))
    cited_pat = Column(String, ForeignKey(Patent.id))

Patent.cited_patents = relationship(Citation, primaryjoin="Patent.id == Citation.citing_pat",
                                    backref=backref('citations', uselist=True, viewonly=True),
                                    viewonly=True)

print(session.query(func.count(Patent.id)).scalar())
for patent in session.query(Patent).filter(Patent.id=='US7294107'):
    print(patent)