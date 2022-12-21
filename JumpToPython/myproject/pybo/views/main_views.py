from ..db import db
from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return redirect(url_for('question._list'))