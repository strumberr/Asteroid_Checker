import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import json

asteroid_name = "2016 FY13"

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

orbit = pyasl.KeplerEllipse(a=0.896, per=0.496, e=0.447, Omega=331, i=1.2, w=77.7)