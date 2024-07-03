import os
import sqlite3


def find_all(sql):
    home_directory = os.path.expanduser('~')
    conn = sqlite3.connect(f'{home_directory}/autoMate.db')
    sql_res = conn.execute(sql)
    res = sql_res.fetchall()
    conn.close()
    return res


def get_config():
    res =  find_all(f"SELECT * FROM config WHERE id = 1")
    return res[0][1]


if __name__ == "__main__":
    print(get_config())