from datetime import date, datetime
import math
from unittest import case
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage
import requests
import os
import random
import time

today = datetime.now()
city = os.environ['CITY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return [weather['weather'], math.floor(weather['high']), math.floor(weather['low']), math.floor(weather['pm25']), weather['airQuality']]

def traffic_restriction():
  year = time.localtime().tm_year
  month = time.localtime().tm_mon
  day = time.localtime().tm_mday
  date = datetime.date(datetime(year, month, day))
  what_day = date.isoweekday()
  if what_day==1:
    return (1, 9)
  elif what_day==2:
    return (2, 8)
  elif what_day==3:
    return(3, 7)
  elif what_day==4:
    return(4, 6)
  elif what_day==5:
    return(5, 0)
  else:
    return None
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather_list = get_weather()
traffic = traffic_restriction()
data = {"weather":{"value":weather_list[0]},"high_temperature":{"value":weather_list[1]}, "low_temperature":{"value":weather_list[2]},"PM25":{"value":weather_list[3]}, "airquality":{"value": weather_list[-1]}, "traffic": {"value": str(traffic[0]) + ", " + str(traffic[1])}, "color":get_random_color()}
print(data)
res = wm.send_template(user_id, template_id, data)
print(res)
