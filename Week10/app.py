import os
import secrets
from contextlib import closing
from flask import Flask, render_template, request, redirect, url_for, session, abort
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or secrets.token_hex(32)

def query(sql, params=(), write=False):
    with closing(mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'capstone_app'),
        password=os.environ['DB_PASSWORD'],
        database=os.getenv('DB_NAME', 'capstone_week10'),
        charset='utf8mb4')) as connection:
        with closing(connection.cursor(dictionary=True)) as cursor:
            cursor.execute(sql, params)
            if write:
                connection.commit()
                return cursor.rowcount
            return cursor.fetchall()

@app.before_request
def protect_form():
    session.setdefault('csrf', secrets.token_hex(32))
    if request.method == 'POST':
        if not secrets.compare_digest(session['csrf'], request.form.get('csrf', '')):
            abort(400, 'Invalid form token')

@app.get('/')
def index():
    rows = query('SELECT id, title, status FROM projects ORDER BY id')
    return render_template('index.html', rows=rows)

def values():
    title = request.form.get('title', '').strip()
    status = request.form.get('status', '')
    if not 1 <= len(title) <= 100 or status not in ('계획', '진행', '완료'):
        abort(400, '프로젝트 명(1~100자)과 상태를 확인하세요.')
    return title, status

@app.post('/projects')
def create():
    query('INSERT INTO projects(title, status) VALUES (%s, %s)', values(), True)
    return redirect(url_for('index'))

@app.post('/projects/<int:project_id>/update')
def update(project_id):
    title, status = values()
    query('UPDATE projects SET title=%s, status=%s WHERE id=%s', (title, status, project_id), True)
    return redirect(url_for('index'))

@app.post('/projects/<int:project_id>/delete')
def delete(project_id):
    query('DELETE FROM projects WHERE id=%s', (project_id,), True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
