from ..db import db
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect , g , flash
from pybo.forms import QuestionForm , AnswerForm

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    ## 빈 딕셔너리 생성, 다양한 정보들을 담기 위해
    question_list= {}
    number = 10
    ## 파라미터 추가할 때는 ?page=
    page = request.args.get('page', type=int, default=1)
    cursor = db.cursor()
    ##sql = 'SELECT * FROM question order by id desc limit {} offset {};'.format(number, number*(page-1))
    
    ## 리스트 페이지에 질문 리스트에 대한 답글 갯수 출력
    sql = """
		select T.* ,u.username from
    (SELECT Q.*, ifnull(A.count, 0) as count
      FROM question AS Q 
      LEFT JOIN (SELECT count(*) AS count, question_id FROM answer GROUP BY question_id) AS A 
      ON Q.id = A.question_id ) as T
      left join user as u on T.user_id = u.id   
    ORDER BY Q.id desc LIMIT {} OFFSET {};
		""".format(number, number * (page - 1))
    cursor.execute(sql)
    item = cursor.fetchall()

    ## 전체 질문게시글 수
    sql = 'SELECT count(* ) as count from question;'
    cursor.execute(sql)
    
    get_len = cursor.fetchone()
    ## 최대 페이지 = 전체 게시글수 -1 을 10으로 나눈 몫에 +1
    max_page = (get_len['count']-1) // number +1
    ## answer 의 전체 데이터 + user 테이블의 username
    question_list['item'] = item
    ## 최대 페이지가 담긴 리스트 생성
    question_list['max_page']= list(range(1,max_page+1))
    question_list['page']= page
    ## 답글 수 계산에 필요
    ## 전체 카운트 - (page-1) * number
    question_list['total']= get_len['count']
    question_list['number'] = number
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    cursor = db.cursor()
    sql = """
    select q.* , u.username  from (SELECT * FROM question WHERE id={}) AS q , user u 
    where q.user_id =u.id;
    """.format(question_id)
    cursor.execute(sql)
    question = cursor.fetchone()
    
    sql = """
    select a.* , u.username  from (SELECT * FROM answer WHERE question_id ={}) AS a  , user u 
    where a.user_id  =u.id
    order by a.create_date desc;
    """.format(question_id)
    cursor.execute(sql)
    answer_set = cursor.fetchall()
    
    return render_template('question/question_detail.html', question=question, answer_set=answer_set, form = form)

@bp.route('/create/', methods=('GET','POST'))
def create():
  if g.user is None:
    return redirect(url_for('auth.login'))
  form = QuestionForm()
  if request.method == "POST" and form.validate_on_submit():
      cursor = db.cursor()
      sql = "insert into question (subject, content, create_date, user_id) values ('{}','{}','{}', {})".format(form.subject.data, 
      form.content.data, datetime.now() , g.user['user_id'])
      cursor.execute(sql)
      db.commit()
      return redirect(url_for('main.index'))
  return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
def modify(question_id):
    cursor = db.cursor()
    sql = "select * from question where id={}".format(question_id)
    cursor.execute(sql)
    question = cursor.fetchone()
    ## 수정 불가
    if g.user['user_id'] != question['user_id']:
       flash('수정권한이 없습니다')
       return redirect(url_for('question.detail', question_id=question_id))
    ## 수정 가능
    print(request.method)
    if request.method == 'POST':  # POST 요청
          form = QuestionForm()
          if form.validate_on_submit():
              cursor = db.cursor()
              sql = "update question set subject='{}', content='{}', modify_date='{}' where id={};".format(form.subject.data, form.content.data, datetime.now(), question_id) 
              cursor.execute(sql)
              db.commit()
              return redirect(url_for('question.detail', question_id=question_id))
    else:  
        # GET 요청 - 기존 본문 내용을 가져온다.
        form = QuestionForm(subject=question['subject'], content=question['content'])
    return render_template('question/question_form.html', form=form)

# myproject/pybo/templates/view/question_views.py

@bp.route('/delete/<int:question_id>')
def delete(question_id):
    cursor = db.cursor()
    sql = "select * from question where id={}".format(question_id)
    cursor.execute(sql)
    question = cursor.fetchone()
    if g.user['user_id'] != question['user_id']:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    sql = "delete from question where id={}".format(question_id)
    cursor.execute(sql)
    db.commit()
    return redirect(url_for('question._list'))