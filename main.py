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


app = Flask('main')
secret_key = os.getenv('SECRET_KEY')

images_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = images_folder

app.secret_key = secret_key

@app.route('/', methods=["GET", "POST"])
def main():

    

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))
    today_replaced = str(today).replace("-", "/")
    tomorrow_replaced = str(tomorrow).replace("-", "/")

    today_tomorrow_date = f"{today_replaced} - {tomorrow_replaced}"

    today = date.today()
    tomorrow = str(datetime.date.today() + datetime.timedelta(1))

    start_date = today
    end_date = tomorrow

    earth_img = os.path.join(app.config['UPLOAD_FOLDER'], 'earth_img.png')


    result = nasa_api(start_date, end_date)

    result2 = sorted(result, key=itemgetter(6))




    print(result)

    
    return render_template("index.html", date=today_tomorrow_date, earth_img=earth_img, result=result2)


@app.route('/asteroid/<variable>', methods=['GET', "POST"])
def asteroid_info(variable):

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

    for el in list_asteroids:
        variable_underscore_slash = f"/{variable_underscore}" 
        if variable_underscore_slash == el["asteroider_name"]["asteroid_link_replaced"]:
            print("true")

            diameter_min = el["asteroider_name"]["asteroid_diameter_min"]
            diameter_max = el["asteroider_name"]["asteroid_diameter_max"]

            diameter_result = (float(diameter_min) + float(diameter_max)) / 2

            asteroid_kmh = el["asteroider_name"]["asteroid_kmh"]
            asteroid_name = el["asteroider_name"]["asteroid_name"]
            asteroid_ID = el["asteroider_name"]["asteroid_ID"]
            asteroid_miss_earth_km = el["asteroider_name"]["asteroid_miss_earth_km"]
            asteroid_approach_time = el["asteroider_name"]["asteroid_approach_time"]
            asteroid_dangerous = el["asteroider_name"]["asteroid_dangerous"]


    
            if os.path.exists(f'static/orbits_models/animated_{variable_underscore}.png'):
                print(f'The file does exist')
                asteroid_orbit = f'/static/orbits_models/animated_{variable_underscore}.png'
            else:
                #set default logo
                print(f'The file does not exist')
                asteroid_orbit = f'/static/orbits_models/animated_{variable_underscore}.gif'



            return render_template("asteroid_info.html", asteroid_orbit=asteroid_orbit, 
                diameter_min=round(diameter_result), 
                asteroid_kmh=round(float(asteroid_kmh)), 
                asteroid_name=asteroid_name, 
                asteroid_ID=asteroid_ID,
                asteroid_miss_earth_km=round(float(asteroid_miss_earth_km)),
                asteroid_approach_time=asteroid_approach_time,
                asteroid_dangerous=asteroid_dangerous)



    return render_template("asteroid_info.html")



@app.route('/sources_of_information', methods=["GET", "POST"])
def information():


    
    return render_template("sources_of_information.html")


scheduler = BackgroundScheduler()
job = scheduler.add_job(render_all_asteroids, 'cron', day_of_week ='mon-sun', hour=1, minute=24)
scheduler.start()


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5550, debug=True, threaded=True)