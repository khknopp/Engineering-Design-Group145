# Kajetan Knopp (khknopp) - 2022

# Main flask imports
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
from arduino import run, connect, read
import asyncio
from plot import plot_all_measurements, plot_sessions
from flask_session import Session


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
    StartDate = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    EndDate = db.Column(db.DateTime, nullable=True)
    Average = db.Column(db.Float)
    Average_F1 = db.Column(db.Float)
    Average_F2 = db.Column(db.Float)
    Average_F3 = db.Column(db.Float)
    Average_F4 = db.Column(db.Float)
    Average_P = db.Column(db.Float)

    def __repr__(self):
        return f"Session: {self.Id}, Score: {self.Average}"
    
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
        return f"Measurement: {self.Id}, Session: {self.Session_Id}, F1: {self.F1}, F2: {self.F2}, F3: {self.F3}, F4: {self.F4}, P: {self.P}"

app.app_context().push()
db.create_all()
global client, char

def update_averages(measurements, sessions):
    # Write code to update the averages of the sessions based on the measurements
    # measurements: list of Measurements objects
    # sessions: list of Sessions objects
    # returns: None
    # Example usage:
    # measurements = Measurements.query.filter_by(Session_Id=session.Id).all()
    # sessions = Sessions.query.all()
    # update_averages(measurements, sessions)
    # db.session.commit()
    for session in sessions:
        measurements = Measurements.query.filter_by(Session_Id=session.Id).all()
        if len(measurements) > 0:
            f1 = []
            f2 = []
            f3 = []
            f4 = []
            p = []
            for measurement in measurements:
                f1.append(measurement.F1)
                f2.append(measurement.F2)
                f3.append(measurement.F3)
                f4.append(measurement.F4)
                p.append(measurement.P)
            session.Average_F1 = sum(f1)/len(f1)
            session.Average_F2 = sum(f2)/len(f2)
            session.Average_F3 = sum(f3)/len(f3)
            session.Average_F4 = sum(f4)/len(f4)
            session.Average_P = sum(p)/len(p)
            session.Average = (session.Average_F1 + session.Average_F2 + session.Average_F3 + session.Average_F4 + session.Average_P)/5
        else:
            session.Average_F1 = 0
            session.Average_F2 = 0
            session.Average_F3 = 0
            session.Average_F4 = 0
            session.Average_P = 0
            session.Average = 0
    db.session.commit()


client, char = 0, 0

@app.route('/', methods=['GET', 'POST'])
def main():
    global char, client, prev
    prev = 0
    if request.method == "POST":
        if 'current' in request.form:
            session = Sessions(Average = 0, Average_F1=0, Average_F2=0, Average_F3=0, Average_F4=0, Average_P=0)
            db.session.add(session)
            db.session.commit()
            return redirect(url_for("current"))
        elif 'progress' in request.form:
            return redirect(url_for("progress"))
    return render_template('index.html')

@app.route('/establish')
async def whatever():
    global client, char
    char, client = await connect()
    print(client, char)
    return "Connection attempted!", 200

@app.route('/current')

async def current(prev=0):
    # char, client = await connect() #i think you want this only once

    if(char and client):
        print("Connected!")
        f1,f2,f3,f4,p = await read(char,client)
        print(f1,f2,f3,f4,p)
        session = Sessions.query.order_by(Sessions.Id.desc()).first()
        measurement = Measurements(Session_Id=session.Id, F1=f1, F2=f2, F3=f3, F4=f4, P=p)
        db.session.add(measurement)
        db.session.commit()
        print("Added measurement!")
    else:
        print("Did not add a measurement!")
    session = Sessions.query.order_by(Sessions.Id.desc()).first()
    try:
        measurements = Measurements.query.filter_by(Session_Id=session.Id).order_by(Measurements.Id.desc()).first()
        print(measurements)
        all_measurements = Measurements.query.filter_by(Session_Id=session.Id).all()
        plot_meas = await plot_all_measurements(all_measurements)
    except:
        print("Does not work")
        measurements = []
        
    prev = 1
    return render_template('current.html', session = session, measurements = measurements, plot_meas=plot_meas)

@app.route('/progress')
def progress():
    sessions = Sessions.query.all()
    all_measurements = Measurements.query.all()

    update_averages(all_measurements, sessions)


    average_session = 0
    for session in sessions:
        average_session += session.Average
    average_session /= len(sessions)

    average_number_of_measurements = 0
    for session in sessions:
        average_number_of_measurements += len(Measurements.query.filter_by(Session_Id=session.Id).all())
    average_number_of_measurements /= len(sessions)

    plot_sess = plot_sessions(sessions)
    return render_template('progress.html', sessions = sessions, plot_sess=plot_sess, number=len(sessions), average_session=round(average_session,2), average_number_of_measurements=round(average_number_of_measurements,2))


if __name__ == '__main__':
    app.run(debug=True)
