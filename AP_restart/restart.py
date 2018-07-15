# coding=utf8
import os
import sys

# 2017.10.30 complete
os.system("curl -d 'speaker=jinho&speed=0&text=공유기를 restart 합니다.' 'https://openapi.naver.com/v1/voice/tts.bin' -H 'Content-Type: application/x-www-form-urlencoded' -H 'X-Naver-Client-Id: wY8qYOdN9FzbBBrgtlF3' -H 'X-Naver-Client-Secret: _dblCskdHA' > restart_restart.mp3")
os.system("omxplayer restart_restart.mp3")

# stop
os.system("sudo service hostapd stop")
os.system("sudo service dnsmasq stop")

# start
# ifdown ifup
os.system("sudo ifdown wlan0; sudo ifup wlan0")

# restart dnsmasq
os.system("sudo service dnsmasq start")

# restart hostapd
os.system("sudo service hostapd start")


os.system("curl -d 'speaker=jinho&speed=0&text=restart가 정상적으로 이루어졌습니다.' 'https://openapi.naver.com/v1/voice/tts.bin' -H 'Content-Type: application/x-www-form-urlencoded' -H 'X-Naver-Client-Id: wY8qYOdN9FzbBBrgtlF3' -H 'X-Naver-Client-Secret: _dblCskdHA' > restart_result.mp3")
os.system("omxplayer restart_result.mp3")
