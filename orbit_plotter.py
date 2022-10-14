import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import json
import os


def asteroid_orbit_calculator(name):
    asteroid_name = name

    r = requests.get(f'https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={asteroid_name}')

    r_dict = r.json()

    json_object = json.dumps(r_dict, indent = 4) 

    print(json_object)

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

    try:
        os.remove("static/orbits_models/plot.png")
    except:
        pass

    orbit = pyasl.KeplerEllipse(a=float(a), per=float(per), e=float(e), Omega=float(omega), i=float(i), w=float(w))
    t = np.linspace(0, 4, 200)

    pos = orbit.xyzPos(t)

    plt.plot(0, 0, 'bo', markersize=9, label="Earth")
    plt.plot(pos[::, 1], pos[::, 0], 'k-', label="Satellite Trajectory")
    plt.plot(pos[0, 1], pos[0, 0], 'r*', label="Periapsis")

    plt.legend(loc="upper right")
    plt.title('Storms Cool Ass Orbital Simulation')

    plt.savefig('static/orbits_models/plot.png')

    ax = plt.gca() #you first need to get the axis handle
    ax.set_aspect(2) #sets the height to width ratio to 1.5. 

asteroid_orbit_calculator("2020 PK7")


