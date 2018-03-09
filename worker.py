import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging
import os

def fetch_data():
	api_key = os.environ.get('WEATHERAPIKEY')  # os.environ.get('WEATHERAPIKEY')

	url = "http://api.wunderground.com/api/{}/conditions/q/NJ/Oceanport.json".format(api_key)
	r = requests.get(url).json()
	data = r['current_observation']

	location = data['display_location']['full']
	weather = data['weather']
	wind_str = data['wind_string']
	temp = data['temp_f']
	humidity = data['relative_humidity']
	precip = data['precip_today_string']
	icon_url = data['icon_url']
	observation_time = data['observation_time']


	# opendb
	try:
		conn = psycopg2.connect(dbname='dedg8mv52hhb6k', user='ktumrtvhijrwwv', host='ec2-54-235-66-24.compute-1.amazonaws.com',
								password='ab34e92bdd8090fb2856d9551f7cae0403caaf5e539d43580dcf3944872e995e')
		print('Opened DB Successfully!')
	except:
		print(datetime.now(), "Unable to connect to database")
		logging.exception('Unable to open the database')
		return
	else:
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# write data to database
	cur.execute("""INSERT INTO weatherapp_reading(location, weather, wind_str, temp, humidity, precip, icon_url,
	observation_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (location, weather, wind_str, temp, humidity, precip,
																  icon_url, observation_time))

	conn.commit()
	cur.close()
	conn.close()

	print("Data Written", datetime.now())
fetch_data()