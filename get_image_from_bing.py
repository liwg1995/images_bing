# -*- coding: utf-8 -*-

import requests
import json
import urllib
import os
import ssl

start_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1516762817652&pid=hp&mkt=zh-CN"
# context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context


def get_url():
    response = requests.get(start_url)
    url = "https://www.bing.com" + response.json()['images'][0]['url']
    image_name = response.json()['images'][0]['copyright'].split('(')[0] + '.jpg'
    # return url, image_name

    file_path = './images'
    try:
        if not os.path.exists(file_path):
            print('文件夹', file_path, '不存在，重新建立')
            os.makedirs(file_path)
        filename = '{}/{}'.format(file_path, image_name)
        urllib.request.urlretrieve(url, filename)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)


if __name__ == '__main__':
    get_url()