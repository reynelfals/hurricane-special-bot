import requests
import config
import os
import csv
import re
import argparse
def sendMessage(chatid, text):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    url_req = "https://api.telegram.org/bot" + config.API_KEY + "/sendMessage" + "?chat_id=" + chatid + "&text=" + text + "&parse_mode=HTML"
    # url_req = "https://api.telegram.org/bot" + config.BOT_KEY + "/sendMessage" + "?chat_id=" + chatid + "&text=" + text
    # url_req = "https://api.telegram.org/bot" + config.BOT_KEY + "/sendPhoto" + "?chat_id=" + chatid

    return requests.get(url_req, headers=headers)
    # return requests.post(url=url_req, data={'photo':open("","rb")})

def sendPhoto(chatid, filename, caption=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # url_req = "https://api.telegram.org/bot" + config.BOT_KEY + "/sendMessage" + "?chat_id=" + chatid + "&text=" + text + "&parse_mode=HTML"
    # url_req = "https://api.telegram.org/bot" + config.BOT_KEY + "/sendMessage" + "?chat_id=" + chatid + "&text=" + text
    url_req = "https://api.telegram.org/bot" + config.API_KEY + "/sendPhoto"
    # headers = {'content-type': 'application/x-www-form-urlencoded'}
    # return requests.get(url_req, headers=headers)
    if caption is None:
        return requests.post(url=url_req, data={'chat_id': chatid}, files={'photo': open(filename, "rb")}, headers=headers)
    return requests.post(url=url_req, data={'chat_id':chatid, 'caption':caption}, files={'photo':open(filename,"rb")}, headers=headers)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('-t', '--text', type=str, action='store', help="Text to send")
    parser.add_argument('-p', '--photo', type=str, action='store', help="Photo filename to send")
    parser.add_argument('-c', '--caption', type=str, action='store', help="Photo caption filename to send")
    args = parser.parse_args()

    for line in args.file:
        if args.text is not None:
            sendMessage(line,args.text)
        if args.photo is not None:
            sendPhoto(line, args.photo, args.caption)





