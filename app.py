# import libraries
from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import pandas as pd
import numpy as np
import requests
import json

# create flask app
app = Flask(__name__)
# connect to database and create cursor to edit
conn = sqlite3.connect("ChelseaFC.db")
c = conn.cursor()
# make tables and columns
c.execute('CREATE TABLE IF NOT EXISTS TopScorers (RK INTEGER, Name TEXT, P INTEGER, G INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS TopAssists (RK INTEGER, Name TEXT, P INTEGER, A INTEGER)')
# save changes and close connection
conn.commit()
conn.close()

# route for homepage
@app.route("/")
def default():
    return render_template('index.html',title='Home')

# route to read data and write to database
@app.route("/data")
def read_data():
    # connect to database
    with sqlite3.connect("ChelseaFC.db") as conn:
        # read table with pandas and create dataframes
        table_data = pd.read_html("https://www.espn.com/soccer/team/stats/_/id/363")
        topScorers = pd.DataFrame(table_data[0],columns=['RK','Name','P','G'])
        topAssists = pd.DataFrame(table_data[1],columns=['RK','Name','P','A'])
        # write to sql and save changes
        topScorers.to_sql('TopScorers',conn,if_exists='replace',index=False)
        topAssists.to_sql('TopAssists',conn,if_exists='replace',index=False)
        conn.commit()

        
    return render_template('data.html',title='Data')

# route to fetch data from database and display
@app.route("/top")
def fetch_top():
    with sqlite3.connect("ChelseaFC.db") as conn:
        allScorers = conn.cursor().execute("SELECT * FROM TopScorers").fetchall()
        allAssists = conn.cursor().execute("SELECT * FROM TopAssists").fetchall()
        
    return render_template('top.html',title='Data',Display0=allScorers,Display1=allAssists)

if __name__ == "__main__":
    app.run(debug=True,port=8100)