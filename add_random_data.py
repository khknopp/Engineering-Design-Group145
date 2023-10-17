from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import random

def add_random_session(db, Session, Measurements):
    start = datetime.datetime.utcnow()
    end = start + datetime.timedelta(minutes=10)
    session = Session(StartDate=start, EndDate=end, Average=45.3, Average_F1=27.7, Average_F2=38.4, Average_F3=10.4, Average_F4=60.45, Average_P=87.3)
    db.session.add(session)
    for i in range(100):
        measurement = Measurements(Session_Id=session.Id, Date=datetime.datetime.utcnow(), F1=random.random(), F2=random.random(), F3=random.random(), F4=random.random(), P=random.random())
        db.session.add(measurement)
    db.session.commit()
    return 1