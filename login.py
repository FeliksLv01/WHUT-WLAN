# coding:utf-8
import logging
import requests
import base64
import re
import sys
import time
import socket

BLUE, END = '\033[1;36m', '\033[0m'

requesr_url = ''

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s ====> %(message)s')

session = requests.Session()
session.trust_env = False


def login_request(username, password) -> bool:
    if not is_net_ok():
        logging.info("your computer is offline，request now...")
        # password = "{B}" + base64.b64encode(password.encode()).decode()  # 加密
        nasId = getNasId()
        logging.info('nasId: ' + str(nasId))
        data = {
            "username": username,
            "password": password,
            "nasId": nasId
        }
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'accept-encoding': 'gzip, deflate',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # if not is_login_as_pc:
        #     headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Mobile Safari/537.36'
        try:
            response = session.post(requesr_url, data=data, headers=headers)
            response.encoding = response.apparent_encoding

            # print(response.text)
            if '"authCode":"ok' in response.text:
                logging.info("login successfully")
                user_ip = get_user_ip(response.text)
                host_ip = get_host_ip()
                logging.info("your user ip: " + user_ip)
                logging.info("your host ip: " + host_ip)
            else:
                logging.error(response.text)
        except Exception:
            logging.exception("requsest error")
    else:
        logging.info("your computer is online  ")
        host_ip = get_host_ip()
        logging.info("your host ip: "+host_ip)

def is_net_ok() -> bool:
    try:
        status = session.get("https://www.baidu.com").status_code
        if status == 200:
            return True
        else:
            return False
    except Exception:
        return False

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_user_ip(response_text):

    match_list = re.findall(r'"UserIpv4":"(.*?)"', response_text, re.S)

    if len(match_list) == 0:
        return -1
    ip = match_list[0]

    return ip


def getNasId() -> int:
    response = session.get(
        'http://www.msftconnecttest.com/redirect?cmd=redirect')
    url = response.url

    response = session.get(url + 'api/config')
    match_list = re.findall(r'"default_nas":"(.*?)"', response.text, re.S)
    if len(match_list) == 0:
        return -1
    nasId_str = match_list[0]
    nasId = int(nasId_str)

    global requesr_url
    requesr_url = url + '/api/account/login'

    return nasId

def heading():
    str = r"""
 _       ____  ____  ________  _       ____    ___    _   __
| |     / / / / / / / /_  __/ | |     / / /   /   |  / | / /
| | /| / / /_/ / / / / / /____| | /| / / /   / /| | /  |/ /
| |/ |/ / __  / /_/ / / /_____/ |/ |/ / /___/ ___ |/ /|  /
|__/|__/_/ /_/\____/ /_/      |__/|__/_____/_/  |_/_/ |_/
"""
    sys.stdout.write(BLUE + str + END + '\n')


if __name__ == "__main__":
    heading()
    args = sys.argv
    username = args[1]
    password = args[2]

    while True:
        try:
            login_request(username, password)
            break
        except:
            logging.exception("Connection refused by the server..")
            logging.exception("Let me sleep for 5 seconds")
            logging.info("ZZzzzz...")
            time.sleep(5)
            logging.info("Was a nice sleep, now let me continue...")
            continue
