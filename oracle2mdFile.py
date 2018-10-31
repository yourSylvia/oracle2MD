"""
直接生成文件
"""

import io
import cx_Oracle as cx
import pandas as pd
import sys

# -*- coding=utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def connect_db(ip, port, sid, username, psd, db_name, path):
    dsn_tns = cx.makedsn(ip, port, sid)
    db = cx.connect(username, psd, dsn_tns)
    print("success")

    # f = open('./demo.md', 'w', encoding='utf-8'
    f = open(path + 'table_structure.md', 'w', encoding='utf-8')
    c = db.cursor()
    c.execute('select TABLE_NAME from all_tables where OWNER = \'%s\'' %db_name)
    table_name_list = c.fetchall()

    for name in table_name_list:
        d = db.cursor()
        d.execute('select comments from user_tab_comments where Table_Name = \'' + name[0] + '\'')
        table_name = d.fetchall()
        if table_name[0][0] is None:
            f.write('表名: ' + name[0] + '\n')
        else:
            f.write('表名: ' + name[0] + '(' + table_name[0][0] + ')' + '\n')

        c.execute(
            'select column_name, data_type, data_length from user_tab_columns where Table_Name = \'' + name[0] + '\'')
        # f.write('| column name |data type|data length|comment|' + '\n')
        # f.write('|:------------:|:-------:|:---------:|:------:|' + '\n')
        f.write('| column name |data type|comment|' + '\n')
        f.write('|:------------:|:-------:|:------:|' + '\n')

        for tup in c.fetchall():
            e = db.cursor()
            string_comm = 'select comments from all_col_comments where Table_Name = \'' + name[
                0] + '\' AND column_name=\'' + tup[0] + '\''
            e.execute(string_comm)
            ans = e.fetchall()
            # if ans[0][0] is None:
            #     f.write('|' + tup[0] + '|' + tup[1] + '|' + str(tup[2]) + '||' + '\n')
            # else:
            #     f.write('|' + tup[0] + '|' + tup[1] + '|' + str(tup[2]) + '|' + ans[0][0] + '|' + '\n')

            if ans[0][0] is None:
                if tup[1] == 'TIMESTAMP(6)':
                    f.write('|' + tup[0] + '|' + tup[1] + '||' + '\n')
                else:
                    f.write('|' + tup[0] + '|' + tup[1] + '(' + str(tup[2]) + ')||' + '\n')
            else:
                if tup[1] == 'TIMESTAMP(6)':
                    f.write('|' + tup[0] + '|' + tup[1] + '||' + '\n')
                else:
                    f.write('|' + tup[0] + '|' + tup[1] + '(' + str(tup[2]) + ')|' + ans[0][0] + '|' + '\n')

    c.close()
    db.close()
    f.close()


def main():
    ip = 'xx.xx.xx.xxx'
    port = xxxx
    sid = 'xxxx'
    username = 'xxxx'
    psd = 'xxxx'
    db_name = 'xxxx'
    path = '/xx/xx/xx/'
    # ip = input("please input ip：")
    # port = input("port：")
    # sid = input("sid：")
    # username = input("username: ")
    # psd = input("psd: ")
    # db_name = input("db_name: ")
    # path = input("output_file_path: ")

    connect_db(ip, port, sid, username, psd, db_name, path)
    print("finish")


if __name__ == "__main__":
    sys.exit(main())