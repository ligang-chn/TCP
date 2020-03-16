# *===================================*
# * Created by LiGang.
# * Author: LiGang
# * Date: 2019/10/25
# * Time: 上午 10:53
# * Project: 整平机控制系统+NB-IoT
# * Power: DATABASE
# *===================================*
import socketserver
import pymysql
import struct
import binascii

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


class Server(socketserver.BaseRequestHandler):
    """服务器端"""

    tcp_data = ""
    taskFlag = False


    def __init__(self, request, client_address, server):
        self.request = request#套接字对象
        self.client_address = client_address#客户端地址信息
        self.server = server#包含调用处理程序的实例
        self.database = Database("localhost", "root", "123456", "info")
        print("[" + self.client_address[0] + "] " + "Connect database successfully.")


        try:
            self.handle()
        finally:
            print("[" + self.client_address[0] + "] " + "End service.")

    def handle(self):
        """定义如何处理每个连接"""
        try:
            print("handle--login****************")
            # res1 = self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES ('LIGANG',23.5,435.4)")
            # print(res1)
            conn = self.request
            conn.sendall(bytes("Connect database successfully.", encoding="utf-8"))
            # Logger('runtime.log', level='info').logger.info('设备已连接>>>' + str(conn))
            while True:#while循环实现多次数据传输
                #从网络上读取的是字节流，数据是bytes，如果我们在代码中要对它做其他操作，就要转成decode()字符str
                #decode():将字节bytes变为字符str
                print("receive data: ")
                ret_bytes= conn.recv(1024)#recv()用于接收数据，接收后转换为字符串便于处理
                while len(ret_bytes)<6:#限制空字符
                    ret_bytes = conn.recv(1024)

                # print(ret_bytes)
                # tuplerec=struct.unpack("!9h",ret_bytes)
                # print(tuplerec)

                # listrec=binascii.hexlify(ret_bytes).decode()#转换成原始16进制字符串，这个和mcu发送的字符一样
                # print(listrec)

                # if(listrec[-1]=='9'):
                #     print(listrec)
                #     break
                ret_str=str(ret_bytes,encoding="utf-8")#ret_bytes.decode("utf-8")
                print(ret_str)
                prt_res = ret_str.split(',')  # 分隔符
                vals=(str(prt_res[0]),float(prt_res[1]),float(prt_res[2]))
                print(vals)
                print("-----------------------")
                print("******start insert*****")
                try:
                    self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s) ", vals)
                # self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s)",vals)
                #     self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s)",vals)
                except Exception as e:
                    print("insert fail!")



                # ret_str=str(ret_bytes,encoding="utf-8")
                #
                #
                #
                # if ret_str=="quit":
                #     # conn.sendall(bytes("Connection dropped",encoding="utf-8"))
                #     print("[quit]<< connection lost")
                #     break
                # elif ret_str=="start#":
                #     #执行数据传输
                #     print("开始传输数据:")
                #     # for row in res:
                #     #     name = row[1]
                #     #     age = row[2]
                #     #     score=row[3]
                #     #     conn.sendall(bytes(str(name)+'|'+str(age)+'|'+str(score),encoding="utf-8"))
                #     #
                #     #     ret_bytes = conn.recv(1024)  # recv()用于接收数据，接收后转换为字符串便于处理
                #     #     ret_str = str(ret_bytes, encoding="utf-8")
                #     #     if ret_str=='0':
                #     #         pass
                #     #     else:
                #     #         conn.sendall(bytes(str(id)+str(name), encoding="utf-8"))
                #
                #
                #
                #     # for row in res:
                #     #     id = row[0]
                #     #     name = row[1]
                #     #     conn.sendall(bytes(id+name, encoding="utf-8"))
                #     #     print(id,name)
                #
                #         # ret_bytes = conn.recv(1024)  # recv()用于接收数据，接收后转换为字符串便于处理
                #         # ret_str = str(ret_bytes, encoding="utf-8")
                #         #
                #         # while ret_str =="fail#":
                #         #     conn.sendall(bytes(id + name, encoding="utf-8"))
                #         #     ret_bytes = conn.recv(1024)  # recv()用于接收数据，接收后转换为字符串便于处理
                #         #     ret_str = str(ret_bytes, encoding="utf-8")
                #         #     if ret_str=="ok#":
                #         #         break
                #     # while True:
                #     #     # 发送数据
                #     #     # print(data.upper())
                #     #     conn.sendall(bytes(res[0] + res[1], encoding="utf-8"))
                # else:
                #     print(ret_str)
                #
                #     # prt_res = ret_str.split(',')  # 分隔符
                #     # print(prt_res)
                #     # print("start insert*****")
                #     # vals=(str(prt_res[0]),float(prt_res[1]),float(prt_res[2]))
                #     # print(vals)
                #     #
                #     # try:
                #     #     self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s) ", vals)
                #     # # self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s)",vals)
                #     # #     self.database.sql_INSERT("INSERT INTO student(name,age,score) VALUES (%s,%s,%s)",vals)
                #     # except Exception as e:
                #     #     print("insert fail!")
                #     # # print("insert success!")


        except Exception as e:
            print(self.client_address, "连接断开")
        finally:
            self.request.close()

    def setup(self):

        print("before handle,连接建立：", self.client_address)

    def finish(self):

        print("finish run  after handle")

if __name__=="__main__":
    HOST,PORT = "172.16.19.77",9999 #私网IP
    print("wait...")
    server=socketserver.ThreadingTCPServer((HOST,PORT),Server)
    # aliDataBase=Database()
    # aliDataBase.sql_INSERT("INSERT INTO student(name,age,score) VALUES ('LIGANG',23.5,435.4)")
    # aliDataBase.sql_INSERT("INSERT INTO student(name,age,score) VALUES ('LIGANG',24,499.1)")

    server.serve_forever()
   #serve_forever()使得程序一直运行，即使一个连接报错了，但不会导致程序停止，而会持续运行，与其他客户端通信






# cursor.execute()
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
# print("Database version : %s " % data)


#
# # 关闭数据库连接
# db.close()

