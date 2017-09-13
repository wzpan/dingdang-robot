# -*- coding:utf-8 -*-
import requests
import json
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

WORDS = ["JIATINGZHUSHOU", "ZHUSHOU"]
SLUG = "homeassistant"


def handle(text, mic, profile, wxbot=None):
    mic.say(u"开始家庭助手控制")
    mic.say(u'请在滴一声后说明内容')
    input = mic.activeListen(MUSIC=True)
    while not input:
        mic.say(u"请重新说")
        input = mic.activeListen(MUSIC=True)
    hass(input, mic, profile)


def hass(text, mic, profile):
    logger = logging.getLogger(__name__)
    if profile[SLUG] or 'url' not in profile[SLUG] or \
       'port' not in profile[SLUG] or \
       'password' not in profile[SLUG]:
        mic.say(u"主人配置有误")
        return
    url = profile[SLUG]['url']
    port = profile[SLUG]['port']
    password = profile[SLUG]['password']
    headers = {'x-ha-access': password, 'content-type': 'application/json'}
    r = requests.get(url+":"+port+"/api/states", headers=headers)
    r_jsons = r.json()
    devices = []
    for r_json in r_jsons:
        entity_id = r_json['entity_id']
        domain = entity_id.split(".")[0]
        if domain not in ["group", "automation", "script"]:
            url_entity = url + ":" + port + "/api/states/" + entity_id
            entity = requests.get(url_entity, headers=headers).json()
            devices.append(entity)
    for device in devices:
        name = device["attributes"]["friendly_name"]
        state = device["state"]
        if name in text:
            device_domain = device["entity_id"].split(".")[0]
            if device_domain == "sensor" or not isAction(text):
                try:
                    measurement = device["attributes"]["unit_of_measurement"]
                except Exception, e:
                    pass
                if 'measurement' in locals().keys():
                    text = text + "状态是" + state + measurement
                    mic.say(text)
                else:
                    text = text + "状态是" + state
                    mic.say(text)
            elif device_domain == "switch" and isAction(text):
                try:
                    if any(word in text for word in [u"开始", u"打开", u"开启"]):
                        newS = "turn_on"
                    elif any(word in text for word in [u"停止", u"结束", u"退出"]):
                        newS = "turn_off"
                    p = json.dumps({"entity_id": device["entity_id"]})
                    url_s = url + ":" + port + "/api/services/switch/" + newS
                    request = requests.post(url_s, headers=headers, data=p)
                    if format(request.status_code) == "200" or \
                       format(request.status_code) == "201":
                        mic.say(u"执行成功")
                    else:
                        mic.say(u"对不起,执行失败")
                        print(format(request.status_code))
                except Exception, e:
                    pass
        break
    else:
        mic.say(u"对不起,指令不存在")


def isAction(text):
    return any(word in text for word in ["打开", "停止", "结束", "开始"])


def isValid(text):
    return any(word in text for word in [u"开启家庭助手",
                                         u"开启助手", u"打开家庭助手", u"打开助手",
                                         u"家庭助手"])
