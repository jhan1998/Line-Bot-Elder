import os

from linebot import LineBotApi, WebhookParser
from dotenv import load_dotenv
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, MessageTemplateAction
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
from linebot.exceptions import LineBotApiError
import requests
from bs4 import BeautifulSoup
import  random
import json


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def push_text_message(user_id, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(user_id, TextSendMessage(text=text))
    return "OK"

def push_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_image_message(reply_token, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_button_message(reply_token, title, text, btn, url):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text='button template',
        template = ButtonsTemplate(
            title = title,
            text = text,
            thumbnail_image_url = url,
            actions = btn
        )
    )
    line_bot_api.reply_message(reply_token, message)

    return "OK"

def crawl_img(title):
    img_name = '長輩圖'
    img_name2 = '+' + title
    url = 'https://www.google.com.tw/search?q='+img_name+img_name2+'+高清&tbm=isch'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    results = soup.find_all("img", {"class": "t0fcAb"})
    index = random.randint(0,20)
    image_links = results[index].get("src")
    return image_links

def crawl_data(search):
    url = 'https://zh-tw.wikipedia.org/wiki/' + search
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    div=soup.find(name='div', id='mw-content-text')
    ps=div.find_all(name='p', limit = 3)
    res = ""
    for p in ps:
        pText=p.get_text()
        res = res + pText
    return res, url

def send_image_carousel(id, imglinks, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)
    cols = []
    for i, url in enumerate(imglinks):
        cols.append(
            ImageCarouselColumn(
                    image_url=url,
                    action=MessageTemplateAction(
                    label=labels[i],
                    text=texts[i]
                )
            )
        )
    message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(columns=cols)
    )
    line_bot_api.push_message(id, message)
    return "OK"

def check_station(station):
    with open('車站基本資料集.json') as f:
        data = json.load(f)

    for i in data:
        if i['stationName'] == station or i['stationEName'].lower() == station:
            return i['stationCode']
    return 'xxxx'

def search_train(station1, station2, time):
    url = 'https://ods.railway.gov.tw/tra-ods-web/ods/download/dataResource/railway_schedule/JSON/list'
    response_post = requests.get(url)
    soup = BeautifulSoup(response_post.text, "lxml")
    res = soup.find_all("a")
    train_url = res[-1].get('href')
    train_res = response_post = requests.get('https://ods.railway.gov.tw/'+train_url)
    json_data = json.loads(train_res.text)
    fromS = station1
    toS = station2
    time = time
    time_fur = int(time[0:2])
    time_fur = time_fur + 2
    search_flag = 0
    result = ''
    result = result + '---------------------------\n'
    for i in json_data['TrainInfos']:
        first_flag = 0
        f_time = ''
        for j in i['TimeInfos']:
            if j['Station'] == fromS[0:4]:
                if j['DEPTime'][0:2] >= time[0:2] and j['DEPTime'][0:2] <= str(time_fur):
                    if j['DEPTime'][0:2] == time[0:2] and j['DEPTime'][3:5] < time[3:5]:
                        break
                    f_time = j['DEPTime']
                    first_flag = 1
                else :
                    break
            if j['Station'] == toS[0:4] and first_flag == 1:
                s_time = j['ARRTime']
                if(i['CarClass'][0:3] == '110'):
                    out = fromS + " 到 " + toS + "\n車種：自強號\n出發時間：" + f_time + "\n抵達時間：" + s_time
                    result = result + out
                    result = result + '\n---------------------------\n'
                elif(i['CarClass'][0:3] == '111'):
                    out = fromS + " 到 " + toS + "\n車種：莒光號\n出發時間：" + f_time + "\n抵達時間：" + s_time
                    result = result + out
                    result = result + '\n---------------------------\n'
                elif(i['CarClass'] == '1131'):
                    out = fromS + " 到 " + toS + "\n車種：區間車\n出發時間：" + f_time + "\n抵達時間：" + s_time
                    result = result + out
                    result = result + '\n---------------------------\n'
                elif(i['CarClass'] == '1132'):
                    out = fromS + " 到 " + toS + "\n車種：區間快車\n出發時間：" + f_time + "\n抵達時間：" + s_time
                    result = result + out
                    result = result + '\n---------------------------\n'
                search_flag = 1
                break
    if(search_flag == 0):
        return ''
    else :
        return result

def send_fsm_graph(reply_token):
    FSM_GRAPH_URL = 'https://i.imgur.com/i90miCx.png'
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url=FSM_GRAPH_URL, preview_image_url=FSM_GRAPH_URL))
    except LineBotApiError as e:
        print(e)




"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
