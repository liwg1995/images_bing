#! /bin/bash

export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin

cd /root/images_bing

python3 insert_to.py

git add images
git commit -m "update"
git push
cd images
rm -rf 2018-*
