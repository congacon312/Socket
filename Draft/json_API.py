import json
import requests

headers={"api_key":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzgzNjY4OTUsImlhdCI6MTYzNzA3MDg5NSwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.0GB2o6aCpphEpDtU7tIMnEhMFkGMF8CXdjF4IyH5bw0"}
exchange_rate = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/sbv",headers)

data = exchange_rate.text

json.loads(data)

print(data)

# exchange_rate.close()

# import urllib.parse
# import urllib.request

# url = "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb"
# header={"results":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzgzNjY4OTUsImlhdCI6MTYzNzA3MDg5NSwic2NvcGUiOiJleGNoYW5nZV9yYXRlIiwicGVybWlzc2lvbiI6MH0.0GB2o6aCpphEpDtU7tIMnEhMFkGMF8CXdjF4IyH5bw0"}

# req = urllib.request.Request(url, header)
# response = urllib.request.urlopen(req)

# print(response.read())

