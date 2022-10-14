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
def daily_post(variable):

    print(variable)

    asteroid_orbit = f'/static/orbits_models/{variable}.png'

    asteroid_orbit_calculator(variable)


    return render_template("asteroid_info.html", asteroid_orbit=asteroid_orbit)








if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5550, debug=True, threaded=True)