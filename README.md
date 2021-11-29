# WHUT_WLAN

武汉理工大学校园网自动登陆脚本

```txt
 _       ____  ____  ________  _       ____    ___    _   __
| |     / / / / / / / /_  __/ | |     / / /   /   |  / | / /
| | /| / / /_/ / / / / / /____| | /| / / /   / /| | /  |/ /
| |/ |/ / __  / /_/ / / /_____/ |/ |/ / /___/ ___ |/ /|  /
|__/|__/_/ /_/\____/ /_/      |__/|__/_____/_/  |_/_/ |_/
```

## 使用方法

安装依赖（目前只有 requests

```shell
pip3 install requests
```

login as PC

```shell
python3 login.py yourNumber yourpassword -pc
```

login as mobile

```shell
python3 login.py yourNumber yourpassword -mobile
```

RasberryPi 文件夹下面是在树莓派下运行的 python 代码以及启动脚本，自动登陆并将 ip 发送到指定邮箱
