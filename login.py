# coding:utf-8
import logging
from os import device_encoding
import requests
import base64
import re
import sys
import time
import socket

BLUE, END = '\033[1;36m', '\033[0m'

requesr_url = ''

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s ====> %(message)s')

session = requests.Session()
session.trust_env = False
device_type = '-pc'

def login_request(username, password) -> bool:
    if not is_net_ok():
        logging.info("your computer is offline，request now...")
        password = "{B}" + base64.b64encode(password.encode()).decode()  # 加密
        ac_id = getAcId()
        # logging.info( 'ac_id: ' + str(ac_id))
        if ac_id == -1:
            logging.error('校园网异常...')
            return False
        data = {
            "action": "login",
            "username": username,
            "password": password,
            "ac_id": ac_id,
            "save_me": 1,
            "ajax": 1
        }
        headersPC = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'accept-encoding': 'gzip, deflate',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'accept-language': 'zh-CN,zh-TW;q=0.8,zh;q=0.6,en;q=0.4,ja;q=0.2',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        headersMobile = {
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Mobile Safari/537.36',
            'accept-encoding': 'gzip, deflate',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'accept-language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        try:
            if(device_type == '-pc'):
                response = session.post(requesr_url, data=data, headers = headersPC)
                #print('login pc')
            else:
                response = session.post(requesr_url, data=data, headers = headersMobile)
                #print('login mobile')
            response.encoding = response.apparent_encoding
            if "login_ok" in response.text:
                logging.info("login successfully")
                ip = get_host_ip()
                logging.info("your ip: "+ip)
            else:
                logging.error(response.text)
        except Exception:
            logging.exception("requsest error")
    else:
        logging.info("your computer is online  ")
        ip = get_host_ip()
        logging.info("your ip: "+ip)


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


# 获取ac_id
def getAcId() -> int:
    response = session.get('http://www.msftconnecttest.com/redirect?cmd=redirect&arubalp=12345')
    # match_list = re.findall(r"<meta http-equiv='refresh' content='1; url=(.*?)'>", response.text, re.S)
    url = response.url
    url = session.get(url).url
    numStr = re.findall(r"index_(.*?).html", url)[0]
    if(device_type == '-pc'):
        url = url.replace('index_' + numStr + '.html?', 'srun_portal_pc.php?ac_id=' + numStr)
    else:
        url = url.replace('index_' + numStr + '.html?', 'srun_portal_phone.php?ac_id=' + numStr)
    response = session.get(url)
    global requesr_url
    requesr_url = 'http://' + re.findall(r'http://(.*?)/srun', url, re.S)[0] +  '/include/auth_action.php'
    match_list = re.findall(r'<input type="hidden" name="ac_id" value="(.*?)">', response.text, re.S)
    if len(match_list) == 0:
        return -1
    ac_id_str = match_list[0]
    ac_id = int(ac_id_str)
    return ac_id


# password必须为编码之前的密码
def logout(username, password):
    postData = {"action": "logout", "username": username, "password": password, "ajax": 1}
    response = session.post(requesr_url, data=postData)
    response.encoding = response.apparent_encoding
    logging.info(response.text)


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
    try:
        device_type = args[3]
        if device_type == '-pc':
            logging.info('login as PC.')
        else:
            logging.info('login as mobile.')
    except:
        logging.info('login as PC.')
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
    #logout(username, password)
