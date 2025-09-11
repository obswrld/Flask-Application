from _datetime import datetime

from flask import Flask, render_template
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
