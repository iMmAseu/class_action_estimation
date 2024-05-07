"""
项目名称：pythonProject
作者：bhml
时间：2022/11/28
代码功能：数据库链接模块
"""

import pymysql


# 数据库链接
def connect_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='1cptbtptp1', database='db_student', charset="utf8")
    cursor = conn.cursor()
    return conn, cursor


# 连接数据库测试
conn, cursor = connect_mysql()
# 查询数据的SQL语句
sql = "SELECT * from users"
# 执行SQL语句
cursor.execute(sql)
# 获取单条查询数据
ret = cursor.fetchall()
cursor.close()
conn.close()
# 打印下查询结果
print(ret)
