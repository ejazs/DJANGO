import requests, time, json
import random
url = "http://localhost:8000/api/v1/create/"
headers = {
  'Content-Type': 'application/json' }

for x in range(1000):
  payload =  {
          "date": "2020-04-16",
          "app_name": "Demo no is {}".format(str(x)),
          "app_start_time": "2020-04-16T12:18:19",
          "app_end_time": "2020-04-16T12:25:19",
          "sys_start_time": "2020-04-16T12:18:19",
          "sys_end_time": "2020-04-16T12:18:19",
          "username": "LAP 370",
          "emp_id": random.randint(10100,25000),
          "sys_uptime": 'null',
          "status": random.choice(['True', 'False']) 
            }


  response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
  print(response.text)
  time.sleep(1)


print('Done')
