import random
import time
from datetime import datetime
import pandas as pd
import sqlite3
    
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return datetime.strptime(time.strftime(time_format, time.localtime(ptime)), '%m/%d/%Y %I:%M')


def random_date(start="10/1/2023 1:30", end="10/30/2023 4:50", prop=random.random()):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M', prop)


df = pd.read_csv('csv/266.csv')
df.rename({
    1: "LATITUDE",
    2: "LONGITUDE"
})

_points = [[row["LATITUDE"], row["LONGITUDE"]] for _, row in df.iterrows()]

points = []
dist = lambda x, y: ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) ** (1/2)
center = (49.83, 24.02)
radius = 0.06
for p in _points:
    if dist(center, p) < radius:
        points.append(p)

for p in points:
    date = random_date(prop=random.random())
    p.append(date)

df = pd.DataFrame(points)
df = df.sort_values(by=[2])


with sqlite3.connect('db/glovo.db') as conn:
    df.to_sql(name='location', con=conn)
