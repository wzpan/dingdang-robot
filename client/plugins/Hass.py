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
    input = input.split(",")[0].split("，")[0]
    hass(input, mic, profile)


def hass(text, mic, profile):
    logger = logging.getLogger(__name__)
    if not profile[SLUG] or 'url' not in profile[SLUG] or \
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
        attributes = device["attributes"]
        domain = device["entity_id"].split(".")[0]
        if 'dingdang' in attributes.keys():
            dingdang = attributes["dingdang"]
            if isinstance(dingdang, list):
                if text in dingdang:
                    try:
                        measurement = attributes["unit_of_measurement"]
                    except Exception, e:
                        pass
                    if 'measurement' in locals().keys():
                        text = text + "状态是" + state + measurement
                        mic.say(text)
                    else:
                        text = text + "状态是" + state
                        mic.say(text)
                    break
            elif isinstance(dingdang, dict):
                if text in dingdang.keys():
                    try:
                        act = dingdang[text]
                        p = json.dumps({"entity_id": device["entity_id"]})
                        s = "/api/services/" + domain + "/"
                        url_s = url + ":" + port + s + act
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


def isValid(text):
    return any(word in text for word in [u"开启家庭助手",
                                         u"开启助手", u"打开家庭助手", u"打开助手",
                                         u"家庭助手"])
