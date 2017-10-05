import configparser
import pymssql

import os
import pypyodbc
from flask import session
from functools import wraps

from config import ROOTDIR


class MSSQL:
    edition = 'Enterprise'

    def __init__(self):
        iniFileUrl = os.path.join(ROOTDIR, 'database', 'database.ini')
        conf = configparser.ConfigParser()  # 生成conf对象
        conf.read(iniFileUrl)  # 读取ini配置文件
        if self.edition == 'Personal':
            print("当前运行模式为单机版")
            section = conf["Personal"]
            self.file = os.path.join(ROOTDIR, section["file"])
            print(self.file)
        else:
            print("当前运行模式为企业版")
            section = conf["Enterprise"]
            self.host = section["host"]
            self.user = section["user"]
            self.pwd = section["pwd"]
            self.db = section["db"]
            if not self.db:
                raise (NameError, "No setting database's information")

    def __GetConnect(self):
        if self.edition == 'Personal':
            self.conn = pypyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + self.file)
            # self.conn=pypyodbc.win_connect_mdb(self.file)
        else:
            self.conn = pymssql.connect(host=self.host,
                                        user=self.user,
                                        password=self.pwd,
                                        database=self.db,
                                        charset="utf8"
                                        )
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "Connection database raises Erro!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def before_req(f):
    @wraps(f)
    def decorated_f(*args, **kwargs):
        if 'edition' not in session:
            print("NO COOKIES!")
            session['edition'] = 'Enterprise'
        print("YES COOKIES! edition:" + session['edition'])
        MSSQL.edition = session['edition']
        return f(*args, **kwargs)

    return decorated_f


# 注意session也可在非视图函数中用，最终传入视图函数，不像request.cookies.get及make_response.set_cookie那般不好用
@before_req
def read_sql(func_name, *args):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(basedir, 'core.sql')
    f = open(file=file, mode='r', encoding='utf-8')
    sql_str = ''
    flag = False
    while True:
        line = f.readline()
        if not line:
            break
        if line.startswith('--end ' + func_name):
            break
        if line.startswith('--start ' + func_name):
            flag = True
            continue
        if line.strip().endswith('*/'):
            continue
        if line.strip().startswith('/*'):
            while flag:
                line = f.readline()
                if line.strip().endswith('*/'):
                    line = ''
                    break
        if flag:
            sql_str = sql_str + line
    f.close()
    sql_str = sql_str.format(*args)
    ms = MSSQL()
    res = ms.ExecQuery(sql_str)
    return res
