from flask import Blueprint
from pymysql import cursors, connect
## 디비 연결정보 명시
db = connect(host='localhost',
             user='root',
             password='admin',
             database='pybo',
             cursorclass = cursors.DictCursor
)
## 디비와의 통신위한 커서 함수 임포트
cursor= db.cursor()
bp = Blueprint ('main',__name__, url_prefix='/')

## / 하위의 라우터들
@bp.route('/')
def hello():
    return 'bp hello'

@bp.route('/bb')
def hello2():
    return 'bbbbbp hello'

    
@bp.route('/user')
def db_User():
    
    sql = "SELECT * FROM question;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return str(result)