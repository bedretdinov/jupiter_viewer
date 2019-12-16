from peewee import *

sqlite_db = SqliteDatabase('data.db', pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = sqlite_db


class Notebooks(BaseModel):
    name = TextField()
    desc = TextField()
    task = TextField()
    exec_interval = TextField()
    file = TextField()
    update_date = TextField()

    class Meta:
        table_name = 'notebooks'
