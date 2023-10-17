import plotly.express as px
import numpy as np
import pandas as pd
import plotly
import json

async def plot_all_measurements(all_measurements):
    # Plot all measurements from a list of database entries
    # all_measurements: list of Measurements objects
    # returns: None
    # Example usage:
    # all_measurements = Measurements.query.filter_by(Session_Id=session.Id).all()
    # plot_all_measurements(all_measurements)
    # plt.show()
    f1 = []
    f2 = []
    f3 = []
    f4 = []
    p = []
    numbering = []
    print(len(all_measurements))
    for measurement in all_measurements:
        print(measurement)
        f1.append(measurement.F1)
        f2.append(measurement.F2)
        f3.append(measurement.F3)
        f4.append(measurement.F4)
        p.append(measurement.P)
    for i in range(len(all_measurements)):
        numbering.append(i)
    df = pd.DataFrame({'x': numbering, 'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'p': p})
    plot = px.line(df, x='x', y=['f1','f2','f3','f4','p'], title='Measurements')
    return json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)
    