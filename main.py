from requesting import nasa_api
from dotenv import load_dotenv
from datetime import date
import datetime
from flask import Flask
from flask import Flask, render_template, request, redirect, flash
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from operator import itemgetter

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


    
  return render_template("index.html", date=today_tomorrow_date, earth_img=earth_img, result=".......")



@app.route('/current-asteroids', methods=["GET", "POST"])
def main2():

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

    for el in result:
      new_el = el[1]
      el_replace = new_el.replace("(", "").replace(")", "").replace(" ", "%")
      link = f"https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr={el_replace}&view=VOPC"
      print(link)

      
    



    print(result)

    
    return render_template("index.html", date=today_tomorrow_date, earth_img=earth_img, result=result2)



if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5550, debug=True, threaded=True)