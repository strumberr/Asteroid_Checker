#import all the necessary packages
from dotenv import load_dotenv
from datetime import date
import datetime
from flask import Flask
from flask import Flask, render_template, request, redirect, flash
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from operator import itemgetter
from orbit_plotter import asteroid_orbit_calculator
from my_requesting import nasa_api
from my_requesting import dict_asteroids
import os 
import os.path
from testing_orbits import render_all_asteroids
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
from math import sqrt


app = Flask('main')
secret_key = os.getenv('SECRET_KEY')

images_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = images_folder

app.secret_key = secret_key

@app.route('/', methods=["GET", "POST"])
def main():

    
    #get the current date and the date tomorrow
    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))
    today_replaced = str(today).replace("-", "/")
    tomorrow_replaced = str(tomorrow).replace("-", "/")

    today_tomorrow_date = f"{today_replaced} - {tomorrow_replaced}"

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))

    start_date = today
    end_date = tomorrow

    #get the earth image
    earth_img = os.path.join(app.config['UPLOAD_FOLDER'], 'earth_img.png')


    result = nasa_api(start_date, end_date)

    result2 = sorted(result, key=itemgetter(6))




    print(result)

    
    return render_template("index.html", date=today_tomorrow_date, earth_img=earth_img, result=result2)


@app.route('/asteroid/<variable>', methods=['GET', "POST"])
def asteroid_info(variable):

    #get today's day and tomorrow's date
    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))
    today_replaced = str(today).replace("-", "/")
    tomorrow_replaced = str(tomorrow).replace("-", "/")

    today_tomorrow_date = f"{today_replaced} - {tomorrow_replaced}"

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))

    start_date = today
    end_date = tomorrow

    print(variable)


    variable_underscore = variable.replace(" ", "_")


    variable_underscore_remove = variable.replace("_", " ")


    list_asteroids = dict_asteroids(start_date, end_date)

    print(list_asteroids)

    #run a for loop to check if the asteroid accessed is in the list, if it matches then get all of the data on the asteroid

    for el in list_asteroids:
        variable_underscore_slash = f"/{variable_underscore}" 
        if variable_underscore_slash == el["asteroider_name"]["asteroid_link_replaced"]:
            print("true")

            #using requests to get data
            diameter_min = el["asteroider_name"]["asteroid_diameter_min"]
            diameter_max = el["asteroider_name"]["asteroid_diameter_max"]

            diameter_result = (float(diameter_min) + float(diameter_max)) / 2

            asteroid_kmh = el["asteroider_name"]["asteroid_kmh"]
            asteroid_name = el["asteroider_name"]["asteroid_name"]
            asteroid_ID = el["asteroider_name"]["asteroid_ID"]
            asteroid_miss_earth_km = el["asteroider_name"]["asteroid_miss_earth_km"]
            asteroid_approach_time = el["asteroider_name"]["asteroid_approach_time"]
            asteroid_dangerous = el["asteroider_name"]["asteroid_dangerous"]

            asteroid_miss_earth_km_rounded = round(float(asteroid_miss_earth_km))


            #get the asteroid ID using the information above and use the sbdb api to look it up
            session2 = requests.Session()
            r2 = session2.get(f'https://ssd-api.jpl.nasa.gov/sbdb.api?spk={asteroid_ID}&phys-par=1')
            r_dict2 = r2.json()
            json_object2 = json.dumps(r_dict2, indent = 4) 
            json_main2 = json.loads(json_object2)

            a2 = json_main2["orbit"]["elements"][1]["value"]
            print(a2)

            #orbit time calculation
            oy = float(a2) ** 3 
            orbit_years = sqrt(oy)

            #length of orbit
            hours_in_time = 8760 * float(orbit_years)
            circumference_orbit = hours_in_time * float(asteroid_kmh)

            #orbit average distance calculation
            e = json_main2["orbit"]["elements"][0]["value"]
            b = sqrt(1-float(e)**2)
            ab = float(a2)/0.000000006684587
            c = ab * b
            print(c)
            average_orbit_distance = (c + ab)/2
            average_orbit_distance_rounded = round(average_orbit_distance)

            first_observed = json_main2["orbit"]["first_obs"]
            last_observed = json_main2["orbit"]["last_obs"]
            source = json_main2["signature"]["source"]


            #check if the orbit animation exists
            if os.path.exists(f'static/orbits_models/animated_{variable_underscore}.png'):
                print(f'The file does exist')
                asteroid_orbit = f'/static/orbits_models/animated_{variable_underscore}.png'
            else:
                #set default logo
                print(f'The file does not exist')
                asteroid_orbit = f'/static/orbits_models/animated_{variable_underscore}.gif'


                asteroid_char = len(asteroid_name)
                asteroid_char_2 = asteroid_char + 7


            #render the template
            return render_template("asteroid_info.html", asteroid_orbit=asteroid_orbit, 
                diameter_min=f"{round(float(diameter_result)):,}",
                asteroid_kmh=f"{round(float(asteroid_kmh)):,}",
                asteroid_name=asteroid_name, 
                asteroid_ID=asteroid_ID,
                asteroid_miss_earth_km=f"{asteroid_miss_earth_km_rounded:,}",
                asteroid_approach_time=asteroid_approach_time,
                asteroid_dangerous=asteroid_dangerous,
                orbit_years=round(orbit_years, 2),
                average_orbit_distance=f"{average_orbit_distance_rounded:,}",
                first_observed=first_observed,
                last_observed=last_observed,
                source=source[-0:-3],
                asteroid_char=asteroid_char_2,
                circumference_orbit=f"{round(circumference_orbit):,}")



    return render_template("asteroid_info.html")







@app.route('/sources_of_information', methods=["GET", "POST"])
def information():


    
    return render_template("sources_of_information.html")


scheduler = BackgroundScheduler()
job = scheduler.add_job(render_all_asteroids, 'cron', day_of_week ='mon-sun', hour=00, minute=2)
scheduler.start()


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5550, debug=True, threaded=True)