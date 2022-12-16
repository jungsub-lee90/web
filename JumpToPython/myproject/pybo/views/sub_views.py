from flask import Blueprint
bp = Blueprint ('sub',__name__, url_prefix='/admin')


## prefix admin 하위의 라우터들
@bp.route('/')
def hello():
    return 'bp sub hello'

@bp.route('/aaa')
def hello2():
    return 'this is a bbbbbp hello'

@bp.route('/bbb')
def hello3():
    return 'this is b bbbbbp hello'