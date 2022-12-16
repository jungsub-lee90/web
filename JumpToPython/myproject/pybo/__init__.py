from flask import Flask

def create_app():
    app = Flask(__name__)

    ## url의 노드들을 카테고리화 할때 블루프린트를 이용해서 핸들링
    from .views import main_views , sub_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(sub_views.bp)
   
    return app