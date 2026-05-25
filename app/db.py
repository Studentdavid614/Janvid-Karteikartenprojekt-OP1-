from sqlmodel import create_engine, SQLModel, Session
from contextlib import contextmanager
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current working directory and from project root when launched via app/main.py.
load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent / '.env')
default_db_path = (Path(__file__).resolve().parent.parent / 'karteikarten.db').as_posix()
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{default_db_path}')

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
