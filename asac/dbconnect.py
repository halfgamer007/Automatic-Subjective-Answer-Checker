from flask_mysqldb import*
def connection():
    conn = MySQLdb.connect(host="localhost",user="root",passwd='1234',db="pbl")
    c=conn.cursor()
    return c, conn