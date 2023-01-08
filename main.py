#! usr/env/python
# coding=utf-8


import string
from sqlite3 import connect

from convert_csv_to_db import WORDS_DB_PATH


class DictionaryData:
    def __init__(self):
        self.conn = connect(WORDS_DB_PATH)
        self.cur = self.conn.cursor()


def search(word, dictionary_data):
    if check_if_english(word):
        dictionary_data.cur.execute(f'SELECT * FROM words where english LIKE "{word}";')
        rows = dictionary_data.cur.fetchall()
        return rows[0]
    else:
        dictionary_data.cur.execute(f'SELECT * FROM words where chinese LIKE "%{word}%";')
        rows = dictionary_data.cur.fetchall()
        return reduce_chinese_result(rows, word)


def check_if_english(word):
    for i in word:
        if i not in string.printable:
            break
    else:
        return True
    return False


def reduce_chinese_result(result_list, word):
    result_list.sort(key=tuple_size)
    for row in result_list:
        for n in row[1].split(","):
            n = n.replace("n.", "").replace("adj.", "")
            if n == word:
                return row
    else:
        return result_list[0]


def tuple_size(tuple):
    return len(tuple[1])


if __name__ == "__main__":
    dict_db = DictionaryData()
    print(search("苹果", dict_db))
