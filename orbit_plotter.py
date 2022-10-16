import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import json
import os
from matplotlib import font_manager
import os.path
from pathlib import Path
import matplotlib
from dotenv import load_dotenv
import pathlib
import pandas as pd
import dropbox
from dropbox.exceptions import AuthError


load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')



def dropbox_connect():

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_upload_file(local_path, local_file, dropbox_file_path):

    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))


matplotlib.use('Agg')

def asteroid_orbit_calculator(name):


    name2 = name.replace(" ", "_")


    asteroid_name = name

    try:

        session = requests.Session()
        
        r = session.get(f'https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={asteroid_name}')

        r_dict = r.json()

        json_object = json.dumps(r_dict, indent = 4) 


        json_main = json.loads(json_object)


        a = json_main["orbit"]["elements"][1]["value"]
        per = json_main["orbit"]["elements"][2]["value"]
        e = json_main["orbit"]["elements"][0]["value"]
        omega = json_main["orbit"]["elements"][4]["value"]
        i = json_main["orbit"]["elements"][3]["value"]
        w = json_main["orbit"]["elements"][5]["value"]


        orbit = pyasl.KeplerEllipse(a=float(a), per=float(per), e=float(e), Omega=float(omega), i=float(i), w=float(w))
        t = np.linspace(0, 4, 200)

        pos = orbit.xyzPos(t)


        #define y-unit to x-unit ratio
        ratio = 1.0
        fig, ax = plt.subplots()

        #get x and y limits
        x_left, x_right = ax.get_xlim()
        y_low, y_high = ax.get_ylim()

        #set aspect ratio
        ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)
        ax.set_facecolor('xkcd:black')

        plt.xlabel("Astronomical units X (au)")
        plt.ylabel("Astronomical units Y (au)")

        #font family
        font_path = 'static/fonts/Space_Grotesk.ttf'  # Your font path goes here
        font_manager.fontManager.addfont(font_path)
        prop = font_manager.FontProperties(fname=font_path)

        plt.rcParams['font.family'] = 'space grotesk'
        plt.rcParams['font.sans-serif'] = prop.get_name()

        plt.plot(0, 0, 'bo', markersize=9, label="Sun", color="blue")
        plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Satellite Trajectory", color="orange")
        plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Periapsis", color="red")

        plt.legend(loc="upper right")
        plt.title(f"{name}'s Orbit")

        name2 = name.replace(" ", "_")

        plt.savefig(f'static/orbits_models/{name2}.png', dpi=300)
        print(f'/static/orbits_models/{name2}.png')


        dropbox_upload_file('static/orbits_models', f'{name2}.png', f'/asteroid_orbits/{name2}.png')


    except:
        return "The link you submitted doesn't correlate to any asteroid on here..."



