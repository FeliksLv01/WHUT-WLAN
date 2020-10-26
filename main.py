# coding:utf-8
import logging
import requests
import base64
import re
import sys
BLUE, END = '\033[1;36m', '\033[0m'

REQUEST_URL = "http://172.30.16.34/include/auth_action.php"
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s ====> %(message)s')


def login_request(username, password):
    # rawPassword = password
    if not is_net_ok():
        logging.info("your computer is offline ， request now... ")
        password = "{B}" + base64.b64encode(password.encode()).decode()  # 加密
        ac_id = getAcId()
        data = {
            "action": "login",
            "username": username,
            "password": password,
            "ac_id": ac_id,
            "save_me": 1,
            "ajax": 1
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
        try:
            response = requests.post(REQUEST_URL, data=data, headers=headers)
            response.encoding = response.apparent_encoding
            if "login_ok" in response.text:
                logging.info("login successfully")
            else:
                logging.error(response.text)
        except Exception:
            logging.exception("requsest error")
    else:
        logging.info("your computer is online  ")


def is_net_ok() -> bool:
    try:
        status = requests.get("https://www.baidu.com").status_code
        if status == 200:
            return True
        else:
            return False
    except Exception:
        return False


# 获取ac_id
def getAcId() -> int:
    response = requests.get('http://hao123.com')
    url = re.findall(r"<meta http-equiv='refresh' content='1; url=(.*?)'>", response.text, re.S)[0]
    url = requests.get(url).url
    numStr = re.findall(r"index_(.*?).html", url)[0]
    url = url.replace('index_' + numStr + '.html', 'srun_portal_pc.php?c_id=' + numStr)
    response = requests.get(url)
    ac_id_str = re.findall(r'<input type="hidden" name="ac_id" value="(.*?)">', response.text,
                           re.S)[0]
    ac_id = int(ac_id_str)
    return ac_id


# password必须为编码之前的密码
def logout(username, password):
    postData = {"action": "logout", "username": username, "password": password, "ajax": 1}
    response = requests.post(REQUEST_URL, data=postData)
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
    login_request(username, password)
    #logout(username, password)
