# import required lib and configs
import requests
from config.cookies import cookies
from config.headers import headers
from config.url import url
from utils.params import getParams

# set params for API, (set size = 1, for start to get the total size of data)
params = getParams(1, 1)

# request API to get data
response = requests.get(url, headers=headers, params=params, cookies=cookies)

# get total number of data available
totalRecords = response.json()["recordsTotal"]

# set the start to 1 and total size of data to 50
start = 1
size = 50

# totalLoop = total number of iteration we have to do to get full data;
totalLoop = (totalRecords // 50) + 1

# intialized an empty array to store data that we got in the loop
data = []

# loop
for i in range(1, totalLoop):
    dataParams = getParams(start, size)
    response = requests.get(url, headers=headers, params=dataParams, cookies=cookies)
    data.append(response.json()["data"])
    start = start + 50

# params = getParams(1, 50)
# response = requests.get(url, headers=headers, params=params, cookies=cookies)
print(len(data[1]))

# data = response.json()['data']
