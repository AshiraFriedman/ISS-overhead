import requests
from datetime import datetime
import smtplib
import time

MY_LAT = '' #enter number here
MY_LONG = '' #enter number here
send_email = ''
receive_email = ''
my_password = ''

def within_iss():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT >= iss_latitude - 5 and MY_LAT <= iss_latitude + 5 and MY_LONG >= iss_longitude - 5 and MY_LONG <= iss_latitude + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True

while True:
    time.sleep(60)
    if within_iss() and is_night():
        with smtplib.SMTP("stmp.gmail.com") as connection:
            connection.starttls()
            connection.login(send_email, my_password)
            connection.sendmail(from_addr=send_email, to_addrs=receive_email, msg="Subject:Look up\n\nThe ISS is above you")


