import requests
from bs4 import BeautifulSoup
import json

duration = []
url = 'https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/railway_schedule/JSON/list'


# 用request.post，並放入form_data
response_post = requests.get(url)
soup = BeautifulSoup(response_post.text, "lxml")
# json_data = json.loads(response_post.text)
res = soup.find_all("a")
train_url = res[-1].get('href')
train_res = response_post = requests.get('https://ods.railway.gov.tw/'+train_url)
json_data = json.loads(train_res.text)
# print(json_data)
# print(type(json_data))
fromS = "4220-台南"
toS = "4340-新左營"
time = '15:30'
result = ''
result = result + '-----------------------------------\n'
for i in json_data['TrainInfos']:
    first_flag = 0
    f_time = ''
    for j in i['TimeInfos']:
        if j['Station'] == fromS[0:4]:
            if j['ARRTime'][0:2] >= '15' and j['ARRTime'][0:2] <= '16':
                if j['ARRTime'][0:2] == '15' and j['ARRTime'][3:5] <= time[3:5]:
                    break
                f_time = j['DEPTime']
                first_flag = 1
            else :
                break
        if j['Station'] == toS[0:4] and first_flag == 1:
            s_time = j['ARRTime']
            if(i['CarClass'][0:3] == '110'):
                out = fromS + " 到 " + toS + "\t車種：自強號\n出發時間：" + f_time + "\n抵達時間：" + s_time
                result = result + out
            elif(i['CarClass'] == '1131'):
                out = fromS + " 到 " + toS + "\t車種：區間車\n出發時間：" + f_time + "\n抵達時間：" + s_time
                result = result + out
            elif(i['CarClass'] == '1132'):
                out = fromS + " 到 " + toS + "\t車種：區間快車\n出發時間：" + f_time + "\n抵達時間：" + s_time
                result = result + out
            result = result + '\n-----------------------------------\n'
            break

print(result)