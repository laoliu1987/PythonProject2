import os
import re
from uuid import uuid1
import requests
from bs4 import BeautifulSoup
from random import choice


# 获取随机请求头
def get_headers():
    file = open('user_agent.txt', 'r')
    user_agent_list = file.readlines()
    user_agent = str(choice(user_agent_list)).replace('\n', '')
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0' if len(
        user_agent) < 10 else user_agent
    headers = {
        "User-Agent": user_agent,
    }
    return headers


# 负责下载图片
def download(src, end):
    try:
        headers = get_headers()
        response = requests.get(src, headers=headers)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        print(img)
        path = "images/" + str(uuid1()) + end
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        with open(path, 'wb') as f:
            f.write(img)
    except Exception as e:
        pass


# 负责请求页面
def requests_get(url):
    try:
        headers = get_headers()
        # 请求页面
        response = requests.get(url, headers=headers)
        # 解析
        soup = BeautifulSoup(response.text, 'lxml')
        image_list = soup.find_all(attrs={"class": "img-responsive"})
        for image in image_list[:-1]:
            # 获取图片链接
            src = image.attrs["data-backup"]
            # 获取图片后缀
            end = os.path.splitext(src)[1]
            if src and end:
                # 去除特殊字符
                end = re.sub(r'[，。?？,/\\·]', '', end)
                # 调用下载函数
                download(src, end)
            else:
                pass
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    # 负责翻页
    for page in range(1, 5):
        url = 'https://www.doutula.com/photo/list/?page=%d' % page
        requests_get(url)