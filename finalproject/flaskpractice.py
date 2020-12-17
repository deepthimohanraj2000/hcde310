from flask import Flask, render_template, request, redirect
import logging
import urllib.parse, urllib.request, urllib.error, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


app = Flask(__name__)

@app.route("/")
def main_handle():
    app.logger.info("In MainHandler")
    return render_template('userinput.html', page_title="Weather Form")

@app.route("/wresponse")
def responese_handler():
    name=request.args.get('city')
    degrees=request.args.get('units')
    numdays=request.args.get('daily')
    numhours=request.args.get('hourly')
    app.logger.info(name)
    unit = ""

    if name != "":
        if numhours=="":
            numhours='48'
        if numdays=="":
            numdays='8'
        if degrees != "":
            if degrees=='Farenheit':
                unit='imperial'
            elif degrees=='Celcius':
                unit='metric'
            else:
                return render_template('userinput.html', page_title="Weather form - Error",
                                       prompt="Please enter a city")
            print(name)
            print(degrees)
            print(type(numdays))
            print(numdays)
            numdays=int(numdays)
            numhours=int(numhours)
            baseurl = 'http://api.openweathermap.org/data/2.5/weather'
            api_key = '486a8ff010ecbbf1754d2e313f7649d4'
            url = baseurl + "?" + "q=" + name + "&appid=" + api_key + "&units=" + unit
            r = urllib.request.urlopen(url)
            weatherstr = r.read()
            weatherdata = json.loads(weatherstr)


            feels_like = (weatherdata['main']['feels_like'])
            temperature = (weatherdata['main']['temp'])
            max_temp = str((weatherdata['main']['temp_max']))
            min_temp = (weatherdata['main']['temp_min'])
            latitude = weatherdata['coord']['lat']
            longitude = weatherdata['coord']['lon']


            baseurl2 = 'https://api.openweathermap.org/data/2.5/onecall?'
            url2 = baseurl2 + "lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=" + api_key + "&units=" + unit
            r2 = urllib.request.urlopen(url2)
            weatherstr2 = r2.read()
            weatherdata2 = json.loads(weatherstr2)


            dailylist=[]
            daysofweek=['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8']
            hourlylist = []
            for dailyw in [weatherdata2][0]["daily"]:
                info = (dailyw['temp']['day'])
                dailylist.append(info)
            dailylist=dailylist[0:numdays]
            daysofweek=daysofweek[0:numdays]
            dailydict = dict(zip(daysofweek, dailylist))


            for hourlyw in [weatherdata2][0]["hourly"]:
                info = hourlyw["temp"]
                hourlylist.append(info)
            hourlylist=hourlylist[0:numhours]

            return render_template('weatheroutput.html', name=name, page_title="Getting current weather for %s"%name,
                               maxtemp=max_temp, mintemp=min_temp, temp=temperature, feelslike = feels_like,
                               latitude=latitude, longitude=longitude, hourlylist=hourlylist, dailydict=dailydict,
                                intnumdays=numdays, numhours=numhours)
        else:
            return render_template('userinput.html', page_title="Weather form - Error", prompt="Please enter a city")
    else:
        return render_template('userinput.html', page_title="Weather form - Error", prompt="Please enter a city")


if __name__=="__main__":
    app.run(host="localhost", port=8080, debug=True)


