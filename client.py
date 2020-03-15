import socket
import pymysql
import time

class Database:
    """
    数据库服务器的地址、账户、密码和库名
    """
    def __init__(self, host="localhost", user="root", password="123456", database="info"):
        try:
            self.db = pymysql.connect(host, user, password, database)#连接数据库
            # 使用 cursor() 方法创建一个游标对象 cursor
            self.cursor = self.db.cursor()#通过cursor来操作数据库,这里cursor没有加括号出现错误
            print("Connect mysql success!")
        except:
            print("Error: connect mysql error")

    def self_sql(self,sql):#执行SQL语句
        """SQL语句执行，可以执行所有SQL语句"""

        try:
            self.cursor.execute(sql)#执行sql语句
            self.db.commit()
            results=self.cursor.fetchall()  # 获得SQL执行返回的所有结果，如果只要SQL执行返回的第一个结果，可用fetchone（）
                                        # SQL执行返回的数据是元组，需要注意处理
            return results
        except:
            print("Error: sel_sql()")
        # for row in data:
        #     id = row[0]
        #     name = row[1]
        #     # 打印结果
        #     print("id=%s,name=%s" % \
        #           (id, name))

    def sql_INSERT(self,sql_insert,val):
        """数据库插入
        eg:
        db.sql_INSERT("INSERT INTO student(name,age,score) VALUES ('LIGANG',23.5,435.4)")
        """
        try:
            self.cursor.execute(sql_insert,val)
            self.db.commit()#提交到数据库
        except:
            self.db.rollback()#如果发生错误，则回滚
            print("ERROR:unable insert")

    def sql_SELECT(self,sql_select):
        """数据库查询
        eg:
        data=db.sql_SELECT("SELECT * FROM student")
        """
        try:
            self.cursor.execute(sql_select)
            #获取所有记录列表
            results=self.cursor.fetchall()
            return results
        except:
            print("Error: unable to fecth data")

    def sql_UPDATE(self,sql_update):
        """数据库更新
        eg:
        db.sql_UPDATE("UPDATE student SET name='liqin' WHERE id=5497")
        """
        try:
            self.cursor.execute(sql_update)
            self.db.commit()
        except:
            self.db.rollback()#发生错误时回滚
            print("ERROR:unable update")

    def sql_DELETE(self,sql_delete):
        """数据库删除(慎用！！！）
        eg:
        db.sql_DELETE("DELETE FROM student WHERE id='5497'")
        """
        try:
            self.cursor.execute(sql_delete)
            self.db.commit()
        except:
            self.db.rollback()#发生错误时回滚
            print("ERROR:unable delete")


class Client:
    """客户端"""


    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.socket = socket.socket()
        self.database = Database("localhost", "root", "123456", "info")

        try:
            self.socket.connect((self.host, self.port))  # 连接服务器
            # 连接成功打印
            cmd_res = self.socket.recv(1024).decode()
            print(cmd_res)
            # self.socket.send(bytes("wait for asking you to start!",encoding="utf-8"))  # 发送数据
        except:
            print("connection failed!")


    def self_Start(self):

        while True:
            cmd = input("(quit退出)>>").strip()  # 去除空字符
            if len(cmd) == 0:
                continue
            if cmd == "quit":
                self.socket.send(cmd.encode("utf-8"))  # 发送数据
                break
            # encode():将str字符转换成指定类型（如utf-8）的字节byte
            self.socket.send(cmd.encode("utf-8"))  # 发送数据
            if cmd=="start#":
                while True:
                    # cmd_res = self.socket.recv(1024)
                    cmd_res=input("start#<<")
                    if cmd_res == "quit":
                        self.socket.send(cmd_res.encode("utf-8"))  # 发送数据
                        break
                    prt_res=cmd_res.split(',')#分隔符
                    print(prt_res)
                    vals=(str(prt_res[0]),float(prt_res[1]),float(prt_res[2]))
                    print(vals)
                    self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s)",vals)

                    self.socket.send(bytes(cmd_res,encoding="utf-8"))  # 发送数据


        #关闭连接
        self.socket.close()


if __name__=="__main__":
    client=Client("121.199.78.48",9999)#公网IP
    # client = Client("127.0.0.1", 9999)  # 公网IP
    # localDB = Database()
    # data = localDB.sql_SELECT("SELECT * FROM student where id=7546")
    # print(data[0].__str__())#元组转换成字符串
    # client.socket.send(bytes(data[0].__str__(), encoding="utf-8"))  # 发送数据
    client.self_Start()









