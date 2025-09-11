from _datetime import datetime

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from typing_extensions import type_repr

app = Flask(__name__)
Scss(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    context = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['context']
        new_task = MyTask(context=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e} ")
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created_at).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id:int):
    deleted_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(deleted_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"


@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.context = request.form['context']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        return "HOME"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
