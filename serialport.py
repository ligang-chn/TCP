import serial #导入模块
import threading
import pymysql


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

    def sql_INSERT(self,sql_insert):
        """数据库插入
        eg:
        db.sql_INSERT("INSERT INTO student(name,age,score) VALUES ('LIGANG',23.5,435.4)")
        """
        try:
            self.cursor.execute(sql_insert)
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




STRGLO="" #读取的数据
BOOL=True  #读取标志位

#读数代码本体实现
def ReadData(ser):
    global STRGLO,BOOL
    # 循环接收数据，此为死循环，可用线程实现
    while BOOL:
        if ser.in_waiting:
            STRGLO = ser.read(ser.in_waiting).decode("gbk")
            print(STRGLO)

#打开串口
# 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
# 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
# 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
def DOpenPort(portx,bps,timeout):
    ret=False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        #判断是否打开成功
        if(ser.is_open):
           ret=True
           threading.Thread(target=ReadData, args=(ser,)).start()
    except Exception as e:
        print("---异常---：", e)
    return ser,ret

#关闭串口
def DColsePort(ser):
    global BOOL
    BOOL=False
    ser.close()

#写数据
def DWritePort(ser,text):
    result = ser.write(text.encode("gbk"))  # 写数据
    return result

#读数据
def DReadPort():
    global STRGLO
    str=STRGLO
    STRGLO=""#清空当次读取
    return str

if __name__=="__main__":

    ser,ret=DOpenPort("COM8",9600,None)
    db=Database()

    if(ret==True):#判断串口是否成功打开
        rec=db.sql_SELECT("SELECT * FROM student WHERE id=7555")
        for row in rec:
            name=row[1]
            age=row[2]
            score=row[3]
        print(str(name)+" "+str(age)+" "+str(score))
        # count=DWritePort(ser,str(name)+str(age)+str(score))
        # print("写入字节数：",count)
        port_data=DReadPort() #读串口数据
        print(port_data)
         # DColsePort(ser)  #关闭串口








































#十六进制处理
# import serial #导入模块
# try:
#   portx="COM3"
#   bps=115200
#   #超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
#   timex=None
#   ser=serial.Serial(portx,bps,timeout=timex)
#   print("串口详情参数：", ser)
#
#   #十六进制的发送
#   result=ser.write(chr(0x06).encode("utf-8"))#写数据
#   print("写总字节数:",result)
#
#   #十六进制的读取
#   print(ser.read().hex())#读一个字节
#
#   print("---------------")
#   ser.close()#关闭串口
#
# except Exception as e:
#     print("---异常---：",e)