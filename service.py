from notebook import execNoteboook
from db import Notebooks
from datetime import datetime, timedelta
from dateutil import parser
import os
import time




while True:

    time.sleep(10)

    notebooks = Notebooks.select()
    for item in notebooks:

        try:
            from_last_update = round((datetime.now() - parser.parse(item.update_date)).seconds / 60)

            if ( from_last_update - int(item.exec_interval) >=0 ):

                UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/notebooks/{0}'
                notebook_list = Notebooks.select().where(Notebooks.file == item.file).execute()

                for item in notebook_list:
                    execNoteboook(UPLOAD_PATH.format(item.file))
                    query = (Notebooks.update(
                        update_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ).where(Notebooks.file == item.file))
                    query.execute()
        except:
            pass