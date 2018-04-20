# -*- coding: utf-8 -*-

import requests
import json
import urllib
import os
import ssl
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import datetime

start_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1516762817652&pid=hp&mkt=zh-CN"
# context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context


def get_url():
    response = requests.get(start_url)
    url = "https://www.bing.com" + response.json()['images'][0]['url']
    print (url)
    image_name = response.json()['images'][0]['copyright'].split('（')[0] + '.jpg'
    print (image_name) 
    # return url, image_name
    time = datetime.datetime.now()

    file_path = './images/{}-{}-{}'.format(time.year, time.month, time.day)
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
     
    dates = '{}-{}-{}'.format(time.year, time.month, time.day)
    qiniu_url = 'https://resources.olei.me/bing_images/{}/'.format(dates) + image_name
    return image_name,url,qiniu_url,dates


def push_qiniu():
    image_name = get_url()[0]

    # 七牛云的accesskey以及secretkey
    access_key = "QxR4DsIF-JaA5-WY4j6JZVnGlS6KUnEubOE5C8HP"
    secret_key = "prMuv9EtxpfjzgOio3_MCiDrj9FEZiZB95na0CDT"

    # 上传至七牛云的文件名
    time = datetime.datetime.now()
    dir = 'bing_images/{}-{}-{}/'.format(time.year, time.month, time.day)
    key = dir + image_name

    # 验证七牛云身份
    q = Auth(access_key, secret_key)

    # 七牛云的存储名字
    bucket_name = "lwg-cunchu"

    # 上传
    token = q.upload_token(bucket_name, key, 3600)
    local_image = "./images/{}-{}-{}/{}".format(time.year, time.month, time.day, image_name)
    ret, info = put_file(token, key, local_image)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(local_image)


    # get_url()
    #push_qiniu()
