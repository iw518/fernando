import pymssql
import pypyodbc

class MSSQL:
    def __init__(self, name='shmged', host="192.168.0.5", user="sa", pwd="58308215", db="shgeodb",file=""):
        self.name = name
        if isinstance(self.name, type(None)):
            raise(NameError, "No setting database's name")
        elif type(self.name) != str:
            raise(NameError, "arg type is erro!")
        else:
            self.host = host
            self.user = user
            self.pwd = pwd
            self.db = db
            filedir="//192.168.0.5/ftp/01-岩土工程部/单机版计算"
            self.file=filedir+"/Tran_shgeodb.mdb"

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "No setting database's information")
        if self.file=='':
            self.conn = pypyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;PWD=;DBQ="+self.file)
        else:
            self.conn = pymssql.connect(host=self.host,
                                        user=self.user,
                                        password=self.pwd,
                                        database=self.db,
                                        charset="utf8"
                                        )
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "Connection database raises Erro!")
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