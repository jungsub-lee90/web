from pymysql import cursors, connect

db = connect(host='localhost',
            user='root',
            password='admin',
            database='pybo',
            cursorclass=cursors.DictCursor)