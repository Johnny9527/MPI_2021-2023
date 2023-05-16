import paho.mqtt.client as mqtt
import random
import json
import datetime
import time

# 設置日期時間的格式
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 連線設定
# 初始化地端程式
client = mqtt.Client()

# 設定登入帳號密碼
client.username_pw_set("mqttuser2","Mqtt123456")

# 設定連線資訊(IP, Port, 連線時間)
client.connect("10.72.55.30", 1883, 60)

while True:
    t0 = random.randint(0,30)
    t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    payload = {'Temperature' : t0 , 'Time' : t}
    print (json.dumps(payload))
    #要發布的主題和內容
    client.publish("topic", json.dumps(payload))
    time.sleep(5)
