import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import matplotlib
import requests
import json
from dotenv import load_dotenv
import os
import dropbox
from dropbox.exceptions import AuthError
import pathlib
from datetime import date
import datetime

load_dotenv()

api_key = os.getenv('API_KEY')

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





def render_all_asteroids():

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))
    today_replaced = str(today).replace("-", "/")
    tomorrow_replaced = str(tomorrow).replace("-", "/")

    today_tomorrow_date = f"{today_replaced} - {tomorrow_replaced}"

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))

    start_date = today
    end_date = tomorrow

    list_asteroid_names = []

    session = requests.Session()
    r4 = session.get(f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}')
    r_dict4 = r4.json()
    json_object4 = json.dumps(r_dict4, indent = 4) 
    json_main4 = json.loads(json_object4)


    for el in json_main4["near_earth_objects"][f"{start_date}"]:
        json_object = json.dumps(el, indent = 4)
        json_all = json.loads(json_object)
        asteroid_name = json_all["name"]
    
        list_asteroid_names.append(asteroid_name)

    for el in json_main4["near_earth_objects"][f"{end_date}"]:
        json_object = json.dumps(el, indent = 4)
        json_all = json.loads(json_object)
        asteroid_name = json_all["name"]
    
        list_asteroid_names.append(asteroid_name)

    
    print(list_asteroid_names)

    el_in_list_asteroid_names = len(list_asteroid_names)
    el_in_list_asteroid_names_new = (float(el_in_list_asteroid_names) * 25) / 60
    print(f"Estimated Render time = {el_in_list_asteroid_names_new} Min.")



    writer = PillowWriter(fps=30)

    asteroid_name = el

    session = requests.Session()

    r = session.get(f'https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={asteroid_name}')

    r_dict = r.json()

    json_object = json.dumps(r_dict, indent = 4) 


    json_main = json.loads(json_object)

    
    for el in list_asteroid_names:

        name_replaced = el.replace(")", "").replace("(", "").replace(" ", "_")

        try:

            if os.path.exists(f'static/orbits_models/animated_{name_replaced}.gif'):
                print(f'The file does exist')
                pass
            else:
                #set default logo
                print(f'The file does not exist')
        

                name_replaced = el.replace(")", "").replace("(", "")

                print(name_replaced)

                writer = PillowWriter(fps=30)

                asteroid_name = name_replaced

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




                t = np.linspace(0, 4, 350)

                

                pos = orbit.xyzPos(t)

                

                plt.style.use('dark_background')
                fig, ax = plt.subplots()
                l = plt.plot(pos[::,1], pos[::,0], 'k-')

                #----------------------------


                #define y-unit to x-unit ratio
                ratio = 1.0
                fig, ax = plt.subplots()

                #get x and y limits
                x_left, x_right = ax.get_xlim()
                y_low, y_high = ax.get_ylim()

                #set aspect ratio
                ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)
                ax.set_facecolor('xkcd:black')

                a2 = 1.00000011
                e2 = 0.01671022
                omega2 = 18.272
                i2 = 0.00005
                w2 = 85.901

                per2 = a2 * (1-e2)


                orbit2 = pyasl.KeplerEllipse(a=float(a2), per=float(per2), e=float(e2), Omega=float(omega2), i=float(i2), w=float(w2))
                t2 = np.linspace(0, 4, 200)

                pos2 = orbit2.xyzPos(t2)


                plt.plot(pos2[::, 1], pos2[::, 0], 'k-', label="Earth Trajectory", color="yellow")
                plt.plot(pos2[0, 1], pos2[0, 0], 'r*', label="Earth Periapsis", color="blue")

                plt.plot(0, 0, 'bo', markersize=9, label="Sun", color="yellow")
                plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Asteroid Trajectory", color="orange", linestyle="dotted")
                plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Asteroid Periapsis", color="gray")


                #----------------------------


                red_dot, = plt.plot(pos[0][1], pos[0][0], 'wo')

                def animate(i):
                    red_dot.set_data(pos[i][1], pos[i][0])
                    return red_dot,

                # create animation using the animate() function
                myAnimation = animation.FuncAnimation(fig, animate,

                                    frames=np.arange(0, len(t), 1), interval=40,

                                    blit=True, repeat=True)


                plt.tick_params(
                    axis='both', 
                    which='both', 
                    bottom=False, 
                    top=False, 
                    labelbottom=False,  
                    left=False,
                    labelleft=False)

                plt.legend(loc="upper right")

                plt.title(f'{asteroid_name} Orbital Simulation')

                name_replaced = el.replace(")", "").replace("(", "").replace(" ", "_")

                myAnimation.save(f'static/orbits_models/animated_{name_replaced}.gif',

                                writer=writer)
                
                dropbox_upload_file('static/orbits_models', f'animated_{name_replaced}.gif', f'/asteroid_orbits_animated/animated_{name_replaced}.gif')
            
        except:
            pass

    