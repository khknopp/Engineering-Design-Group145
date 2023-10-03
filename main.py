# Kajetan Knopp (khknopp) - 2022

# Main flask imports
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime

# Training import
from training import *

# Main flask definitions
app = Flask(__name__)
app.secret_key = "squishstickprivatekey"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

# Database definition
db = SQLAlchemy(app)

class Sessions(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    Average = db.Column(db.Float, nullable=False)
    Average_F1 = db.Column(db.Float, nullable=False)
    Average_F2 = db.Column(db.Float, nullable=False)
    Average_F3 = db.Column(db.Float, nullable=False)
    Average_F4 = db.Column(db.Float, nullable=False)
    Average_P = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Session: {self.Id}, Date: {self.Date}, Score: {self.Average}"
    
class Measurements(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Session_Id = db.Column(db.Integer, db.ForeignKey('sessions.Id'), nullable=False)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    F1 = db.Column(db.Float, nullable=False)
    F2 = db.Column(db.Float, nullable=False)
    F3 = db.Column(db.Float, nullable=False)
    F4 = db.Column(db.Float, nullable=False)
    P = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Measurement: {self.Id}, Session: {self.Session_Id}, Date: {self.Date}, F1: {self.F1}, F2: {self.F2}, F3: {self.F3}, F4: {self.F4}, P: {self.P}"

app.app_context().push()


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if 'current' in request.form:
            return redirect(url_for("current"))
        elif 'progress' in request.form:
            return redirect(url_for("progress"))
    return render_template('index.html')

@app.route('/current')
def current():
    session = Sessions.query.order_by(Sessions.Id.desc()).first()
    try:
        measurements = Measurements.query.filter_by(Session_Id=session.Id).all()
    except:
        measurements = []
    return render_template('current.html', session = session, measurements = measurements)

@app.route('/progress')
def progress():
    sessions = Sessions.query.all()
    return render_template('progress.html', sessions = sessions)


if __name__ == '__main__':
    app.run(debug=True)
