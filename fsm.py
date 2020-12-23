from transitions.extensions import GraphMachine

from utils import send_text_message, push_text_message, send_button_message, send_image_message, crawl_img, send_image_carousel, crawl_data, check_station, search_train, send_fsm_graph
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction
import time

class TocMachine(GraphMachine):
    from_station = ''
    to_station = ''
    name1 = ''
    name2 = ''
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **{
                "states" : [
                    'init',
                    'option',
                    'elder',
                    'knowledge',
                    'greet',
                    'reply_greet',
                    'festival',
                    'reply_festival',
                    'wish',
                    'reply_wish',
                    'replydata',
                    'train',
                    'station',
                    'search',
                    'fsm'
                ],
                "transitions" : [
                    {
                        'trigger': 'advance',
                        'source': 'init',
                        'dest': 'option',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'option',
                        'dest': 'elder',
                        'conditions': 'is_going_to_elder',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'elder',
                        'dest': 'elder',
                        'conditions': 'is_going_to_echo',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'elder',
                        'dest': 'greet',
                        'conditions': 'is_going_to_greet',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'greet',
                        'dest': 'reply_greet',
                        'conditions': 'is_going_to_reply_greet',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'elder',
                        'dest': 'festival',
                        'conditions': 'is_going_to_festival',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'festival',
                        'dest': 'reply_festival',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'elder',
                        'dest': 'wish',
                        'conditions': 'is_going_to_wish',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'wish',
                        'dest': 'reply_wish',
                    },
                    {
                        'trigger': 'advance',
                        'source': ['reply_greet', 'reply_festival', 'reply_wish', 'replydata', 'search', 'fsm'],
                        'dest': 'option',
                        'conditions': 'is_going_to_option',
                    },
                    {
                        'trigger': 'advance',
                        'source': ['reply_greet', 'reply_festival', 'reply_wish'],
                        'dest': 'elder',
                        'conditions': 'is_going_to_restart',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'option',
                        'dest': 'knowledge',
                        'conditions': 'is_going_to_knowledge',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'elder',
                        'dest': 'option',
                        'conditions': 'is_going_to_option',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'knowledge',
                        'dest': 'replydata',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'replydata',
                        'dest': 'knowledge',
                        'conditions': 'is_going_to_restartK',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'option',
                        'dest': 'train',
                        'conditions': 'is_going_to_train',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'train',
                        'dest': 'station',
                        'conditions': 'is_going_to_station',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'station',
                        'dest': 'search',
                        'conditions': 'is_going_to_station2',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'train',
                        'dest': 'train',
                        'conditions': 'is_going_to_reenter',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'station',
                        'dest': 'station',
                        'conditions': 'is_going_to_reenter',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'search',
                        'dest': 'train',
                        'conditions': 'is_going_to_restart',
                    },
                    {
                        'trigger': 'advance',
                        'source': 'option',
                        'dest': 'fsm',
                        'conditions': 'is_going_to_fsm'
                    },
                    {
                        'trigger': 'advance',
                        'source': 'option',
                        'dest': 'option',
                        'conditions': 'echo',
                    },
                    {"trigger": "go_back_knowledge", "source": ['replydata'], "dest": "knowledge"},
                ],
                "initial" : 'init',
                "auto_transitions" : False,
                "show_conditions" : True,
            }
        )

    def is_going_to_option(self, event):
        if event.message.text.lower() == "menu":
            return True

    def is_going_to_elder(self, event):
        return event.message.text.lower() == "elder image" or event.message.text.lower() == "elder image "
    
    def is_going_to_greet(self, event):
        return event.message.text == "問候"
    
    def is_going_to_reply_greet(self, event):
        return event.message.text == "早安" or event.message.text == "午安" or event.message.text == "晚安"

    def is_going_to_festival(self, event):
        return event.message.text == "節慶"

    def is_going_to_wish(self, event):
        return event.message.text == "祝福"

    def is_going_to_train(self, event):
        return event.message.text.lower() == "train" or event.message.text.lower() == "train "

    def is_going_to_station(self, event):
        s = event.message.text
        if s[0] == '台':
            s = '臺' + s[1:]
        num = check_station(s)
        if num == 'xxxx':
            return False
        else :
            self.from_station = num
            self.name1 = event.message.text
            return True

    def is_going_to_station2(self, event):
        s = event.message.text
        if s[0] == '台':
            s = '臺' + s[1:]
        num = check_station(s)
        if num == 'xxxx' and num != self.from_station:
            return False
        else :
            self.to_station = num
            self.name2 = event.message.text
            return True

    def is_going_to_reenter(self, event):
        push_text_message(event.source.user_id, "錯誤輸入請再試一次")
        return True

    def echo(self, event):
        print("echo")
        reply_text = "請重新輸入"
        push_text_message(event.source.user_id, reply_text)
        return True

    def is_going_to_echo(self, event):
        if event.message.text != "問候" and event.message.text != "節慶" and event.message.text != "祝福":
            push_text_message(event.source.user_id, "請重新輸入")
            return True
    
    def is_going_to_restart(self, event):
        if event.message.text.lower() == "restart":
            return True
        else :
            push_text_message(event.source.user_id, "請重新輸入")
            return False

    def is_going_to_restartK(self, event):
        if event.message.text.lower() == "restart":
            return True
        else :
            push_text_message(event.source.user_id, "請重新輸入")
            return False

    def is_going_to_knowledge(self, event):
        return event.message.text.lower() == "knowledge" or event.message.text.lower() == "knowledge "

    def is_going_to_fsm(self, event):
        return event.message.text.lower() == "fsm" or event.message.text.lower() == "fsm "

    def on_enter_option(self, event):
        print("I'm entering option")
        reply_text = "輸入『 Elder Image 』即可開始搜尋長輩圖。\n輸入『 Knowledge 』來了解一些老年疾病知識。\n輸入『train』來查詢火車時刻。\n輸入『 FSM 』來查看狀態圖。"
        push_text_message(event.source.user_id, reply_text)
        send_image_message(event.reply_token, "https://i0.wp.com/www.saydigi.com/wp-content/uploads/2018/05/8ce003614e9ce281ed5b881d1e388167.png")

    def on_exit_option(self, event):
        print("Leaving option")

    def on_enter_elder(self, event):
        print("I'm entering elder")
        # reply_text = "馬上依照您的需求搜尋長輩圖！\n請輸入您的用途。"
        # send_text_message(event.reply_token, reply_text)
        title = '馬上依照您的需求搜尋長輩圖！'
        text = '請輸入您的用途'
        btn = [
            MessageTemplateAction(
                label = '問候',
                text ='問候'
            ),
            MessageTemplateAction(
                label = '節慶',
                text ='節慶'
            ),
            MessageTemplateAction(
                label = '祝福',
                text = '祝福'
            ),
        ]
        url = 'https://i.imgur.com/ICK2lr1.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        push_text_message(event.source.user_id,"請選擇以上選項或輸入『問候』，『節慶』或『祝福』")

    def on_enter_greet(self, event):
        print("I'm entering greet")
        title = '請選擇『早安』, 『午安』, 『晚安』'
        text = ' '
        btn = [
            MessageTemplateAction(
                label = '早安',
                text ='早安'
            ),
            MessageTemplateAction(
                label = '午安',
                text ='午安'
            ),
            MessageTemplateAction(
                label = '晚安',
                text = '晚安'
            ),
        ]
        url = 'https://i.imgur.com/ICK2lr1.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        push_text_message(event.source.user_id,"請選擇以上選項或輸入『早安』，『午安』或『晚安』")

    def on_enter_reply_greet(self, event):
        print("I'm entering reply greet")
        # reply_text = "你選擇『" + event.message.text + "』。"
        push_text_message(event.source.user_id, "你選擇『"+ event.message.text +"』。")
        url = crawl_img(event.message.text)
        send_image_message(event.reply_token, url)
        # reply_text = "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』"
        push_text_message(event.source.user_id, "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』")
    
    def on_enter_festival(self, event):
        print("I'm entering festival")
        reply_text = "請輸入節日。"
        send_text_message(event.reply_token, reply_text)
    
    def on_enter_reply_festival(self, event):
        print("I'm entering reply festival")
        # reply_text = "你輸入『" + event.message.text + "』。"
        push_text_message(event.source.user_id, "你輸入『"+ event.message.text + "』。")
        url = crawl_img(event.message.text)
        send_image_message(event.reply_token, url)
        # reply_text = "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』"
        push_text_message(event.source.user_id, "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』")
    
    def on_enter_wish(self, event):
        print("I'm entering wish")
        reply_text = "請輸入想祝福的話。"
        send_text_message(event.reply_token, reply_text)

    def on_enter_reply_wish(self, event):
        print("I'm entering reply wish")
        # reply_text = "你輸入『" + event.message.text + "』。"
        push_text_message(event.source.user_id, "你輸入『"+ event.message.text +"』。")
        url = crawl_img(event.message.text)
        send_image_message(event.reply_token, url)
        # reply_text = "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』"
        push_text_message(event.source.user_id, "對這次產生的長輩圖滿意嗎？\n想要再次搜尋請輸入『restart』\n想回到主選單請輸入『menu』")

    def on_enter_knowledge(self, event):
        print("I'm entering knowledge")
        userid = event.source.user_id
        
        stroke = 'https://th.bing.com/th/id/OIP.Hcg2yHN2B5GhEDb-WLt-EgHaHr?o=6&pid=Api&rs=1'
        heart = 'https://d2e7nuz2r6mjca.cloudfront.net/2018/7/1532539267_W1-1280w.jpg'
        press = 'https://i1.wp.com/www.doublefitness.com.tw/wp-content/uploads/2019/07/%E9%AB%98%E8%A1%80%E5%A3%93%E5%8E%9F%E5%9B%A0.jpg?fit=1052%2C822&ssl=1'
        sugar = 'https://pic2.zhimg.com/v2-451fc0c170362be97207e1d76848bf25_r.jpg?source=172ae18b'
        ost = 'https://i.ytimg.com/vi/_xMxXF9od5E/maxresdefault.jpg'
        urls = [stroke, heart, press, sugar, ost]
        labels = ['中風', '冠心病', '高血壓', '糖尿病', '骨質酥鬆']
        texts = ['中風', '冠心病', '高血壓', '糖尿病', '骨質酥鬆']
        send_image_carousel(userid, urls, labels, texts)
        push_text_message(event.source.user_id, "請選擇上述資訊，或直接輸入疾病名稱")

    def on_enter_replydata(self, event):
        print("reply")
        check = "\n维基百科目前还没有与上述标题相同的条目。"
        res, url = crawl_data(event.message.text)
        if res[0:6] != check[0:6]:# print(res)
            send_text_message(event.reply_token, res)
            push_text_message(event.source.user_id, "此為部分資料想知道更多請參閱以下網址\n" + url)
            push_text_message(event.source.user_id, "想了解更多資訊請輸入『restart』\n想回到目錄請輸入『menu』")
        else:
            push_text_message(event.source.user_id, "查無此病，請再試一次")
            self.go_back_knowledge(event)

    def on_enter_train(self, event):
        push_text_message(event.source.user_id, "馬上為您查詢火車班次，請依照以下格式輸入出發站：\nYY(中文或英文站名)")

    def on_enter_station(self, event):
        push_text_message(event.source.user_id, "請依照以下格式輸入抵達站：\nYY(中文或英文站名)")

    def on_enter_search(self, event):
        station1 = self.from_station + '-' + self.name1
        station2 = self.to_station + '-' + self.name2
        t = time.strftime('%H:%M:%S', time.localtime())
        print(t)
        res = search_train(station1, station2, t)
        if res == '':
            push_text_message(event.source.user_id, '為搜尋到任何附近班次')
        else:
            push_text_message(event.source.user_id, res)
        push_text_message(event.source.user_id, "想查詢更多班次請上台鐵官網查詢\nhttps://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime")
        push_text_message(event.source.user_id, "想了解更多資訊請輸入『restart』\n想回到目錄請輸入『menu』")

    def on_enter_fsm(self, event):
        send_fsm_graph(event.reply_token)
