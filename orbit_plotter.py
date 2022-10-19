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

REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

APP_KEY = os.getenv('APP_KEY')

APP_SECRET = os.getenv('APP_SECRET')


def dropbox_connect():

    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_upload_file(local_path, local_file, dropbox_file_path):

    dbx = dropbox.Dropbox(
            app_key = APP_KEY,
            app_secret = APP_SECRET,
            oauth2_refresh_token = REFRESH_TOKEN
        )


    try:
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
        print(a)
        print(per)
        print(e)
        print(omega)
        print(i)
        print(w)

        


        orbit = pyasl.KeplerEllipse(a=float(a), per=float(per), e=float(e), Omega=float(omega), i=float(i), w=float(w))
        t = np.linspace(0, 4, 200)

        pos = orbit.xyzPos(t)



        a2 = 1.00000011
        e2 = 0.01671022
        omega2 = 18.272
        i2 = 0.00005
        w2 = 85.901

        per2 = a2 * (1-e2)


        orbit2 = pyasl.KeplerEllipse(a=float(a2), per=float(per2), e=float(e2), Omega=float(omega2), i=float(i2), w=float(w2))
        t2 = np.linspace(0, 4, 200)

        pos2 = orbit2.xyzPos(t2)


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

        plt.plot(pos2[::, 1], pos2[::, 0], 'k-', label="Earth Trajectory", color="yellow")
        plt.plot(pos2[0, 1], pos2[0, 0], 'r*', label="Earth Periapsis", color="blue")

        plt.plot(0, 0, 'bo', markersize=3, label="Sun", color="yellow")
        plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Asteroid Trajectory", color="orange")
        plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Asteroid Periapsis", color="gray")


        plt.legend(loc="lower right", fontsize='xx-small', facecolor='black', labelcolor='white')
        plt.title(f"{name}'s Orbit")

        name2 = name.replace(" ", "_")

        plt.savefig(f'static/orbits_models/earth_{name2}.png', dpi=300)
        print(f'/static/orbits_models/{name2}.png')


        dropbox_upload_file('static/orbits_models', f'earth_{name2}.png', f'/asteroid_orbits/earth_{name2}.png')


    except:
        return "The link you submitted doesn't correlate to any asteroid on here..."