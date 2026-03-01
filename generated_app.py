from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# サンプルデータ
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

# templatesディレクトリとHTMLファイルを作成
if not os.path.exists('templates'):
    os.makedirs('templates')

html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .container { max-width: 600px; }
        .task { padding: 10px; margin: 5px 0; background: #f0f0f0; border-radius: 5px; }
        .delete-btn { color: red; text-decoration: none; float: right; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Todo List</h1>
        
        <form action="/add" method="POST">
            <input type="text" name="task" placeholder="新しいタスクを入力" required>
            <button type="submit">追加</button>
        </form>
        
        <div>
            {% for task in tasks %}
            <div class="task">
                {{ task }}
                <a href="/delete/{{ loop.index0 }}" class="delete-btn">削除</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>'''

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

if __name__ == '__main__':
    app.run(debug=True)