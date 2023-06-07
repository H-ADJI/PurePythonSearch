from collections import Counter
from datetime import datetime

from sqlmodel import Field, Session, SQLModel, create_engine, select

from search_engine.data_processing import tokenize


class Jobs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    linkedin_id: str
    title: str
    description: str
    url: str = None
    seniority: str = None
    employement_type: str = None
    function: str = None
    industry: str = None
    posting_date: datetime = None
    location: str = None
    company_name: str = None
    company_id: str = None
    company_url: str = None

    @property
    def full_text(self):
        return self.title + " " + self.description

    @property
    def clean_tokens(self):
        return tokenize(self.full_text)

    def term_frequency(self, term):
        return Counter(self.clean_tokens).get(term, 0)


# Create the SQLite engine handling the connection with the db
engine = create_engine("sqlite:///jobs.db")
# Create the tables
SQLModel.metadata.create_all(engine)


def job_generator(size: int = 20) -> Jobs:
    with Session(bind=engine) as db_session:
        query = select(Jobs).limit(size)
        jobs = db_session.exec(query)
        for job in jobs:
            yield job


def get_job_by_id(id: int) -> Jobs:
    with Session(bind=engine) as db_session:
        query = select(Jobs).where(Jobs.id == id)
        return db_session.exec(query).first()
