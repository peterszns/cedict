#! usr/env/python
# coding=utf-8


import string
import os
from sqlite3 import connect

import csv


class DbSetup:
    def __init__(self):
        # self.del_db_if_exists()
        self.words_db_path = './db/words.db'
        self.conn = connect(self.words_db_path)
        self.cur = self.conn.cursor()

    def del_db_if_exists(self):
        if os.path.exists('./db/words.db'):
            os.remove('./db/words.db')

    def setupdb(self):
        print('creating table for words')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS words (english TEXT, chinese TEXT)''')

        print('inserting EnWords csv into database')
        with open('./EnWords.csv', 'r', encoding="utf8") as f:
            dr = csv.reader(f)
            for index, i in enumerate(dr):
                if index == 0:
                    continue
                print('inserting ' + str(i))
                self.cur.execute('INSERT INTO words VALUES (?,?);', i)

        self.cur.execute('SELECT * FROM words')
        rows = self.cur.fetchall()
        for row in rows:
            print('QUERY ALL: ' + str(row))

        self.conn.commit()
        self.conn.close()

    def search(self, word):
        if self.check_if_english(word):
            self.cur.execute(f'SELECT * FROM words where english LIKE "{word}";')

            rows = self.cur.fetchall()
            for row in rows:
                return row
        else:
            self.cur.execute(f'SELECT * FROM words where chinese LIKE "%{word}%";')
            rows = self.cur.fetchall()

            return self.reduce_chinese_result(rows, word)

    def check_if_english(self, word):
        for i in word:
            if i not in string.printable:
                break
        else:
            return True
        return False

    def reduce_chinese_result(self, result_list, word):
        result_list.sort(key=self.tuple_size)
        for row in result_list:
            for n in row[1].split(","):
                n = n.replace("n.", "").replace("adj.", "")
                if n == word:
                    return row
            else:
                return result_list[0]
        else:
            return result_list[0]

    def tuple_size(self, tuple):
        return len(tuple[1])


if __name__ == "__main__":
    ds = DbSetup()
    # ds.setupdb()
    print(ds.search("beautiful"))
