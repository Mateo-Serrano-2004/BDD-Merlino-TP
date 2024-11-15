from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, User, insert_user_mongo, get_users_mongo

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users_sqlite = User.query.all()

    users_mongo = get_users_mongo()

    return render_template('index.html', users_sqlite=users_sqlite, users_mongo=users_mongo)

@main.route('/add_sqlite', methods=['POST'])
def add_sqlite():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('main.index'))

@main.route('/add_mongo', methods=['POST'])
def add_mongo():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        insert_user_mongo(username, email)
        
        return redirect(url_for('main.index'))
