#! usr/env/python
# coding=utf-8


import os
from sqlite3 import connect

import csv

WORDS_DB_PATH = './db/words.db'
WORDS_CSV_PATH = "./csv/EnWords.csv"


class DbSetup:
    def __init__(self):

        self.del_db_if_exists()

        self.conn = connect(WORDS_DB_PATH)
        self.cur = self.conn.cursor()

    def del_db_if_exists(self):
        if os.path.exists(WORDS_DB_PATH):
            os.remove(WORDS_DB_PATH)

    def setup(self):
        print('creating table for words')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS words (english TEXT, chinese TEXT)''')

        print('inserting EnWords csv into database')
        with open(WORDS_CSV_PATH, 'r', encoding="utf8") as f:
            csv_content = csv.reader(f)
            for index, i in enumerate(csv_content):
                if index == 0:
                    continue
                print('inserting ' + str(i))
                self.cur.execute('INSERT INTO words VALUES (?,?);', i)

        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    ds = DbSetup()
    ds.setup()
