221216

JumpToPython/activate -> basic config before flask run. 
  - Set init file
  - set debug mode before flask run
  - run activate original file

JumpToPython/pybo_env/requirements.txt. -> dump used lib for team project
  1. pip freeze -> check the used lib lists.
  2. pip freeze freeze.txt -> create txt file with lib lists.
  3. pip install -r freeze.txt -> deploy the lists for new env.
 
JumpToPython/pybo_env -> virtual environment create
  1. C:\JumpToPython> python -m venv pybo_env
  2. win > source /Document/Github/JumpToPython/pybo_env/Scripts/activate
     mac > source /Document/Github/JumpToPython/pybo_env/bin/activate
     (if not using) deactivate

flask web baseline structure
JumpToPython
  ├── pybo/
  │      ├─ __init__.py.        -> flask init
  │      ├─ models.py           -> database connections
  │      ├─ forms.py            -> html form through logic
  │      ├─ views/              -> categorical router views
  │      │   └─ main_views.py
  │      ├─ static/             -> css, js , image, etc files
  │      │   └─ style.css
  │      └─ templates/          -> html files
  │            └─ index.html
  └── config.py                 -> various variables defined
  
  ----------
  TIL 
   1. aplication factory -> separation a flask init file(default) to a folder. flask seeks the init file in a specific directory
   2. flask blueprint func -> categorize the routing point. init.py only call views
   3. mysql db data retrive query test.
      - import cursors and connect using pymysql lib
      - db info desc into connect()
      - db.cursor() -> cursor activate for db communication
      - db.cursor().excute(sql query)
      - cursor.fetch() -> data retrive when return the data format must be str
  
