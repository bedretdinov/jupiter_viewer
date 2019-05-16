from db import SqlLite

sql = SqlLite()

sql.query('''
    DROP TABLE notebooks
''')

sql.query('''
    CREATE TABLE notebooks
             (name text, desc text, task text, exec_interval int, file text, update_date text )
''')


