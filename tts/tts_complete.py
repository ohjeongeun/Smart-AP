# coding=utf8
import sys
import os

# 2017.11.10 completed
os.system("curl -d 'speaker=jinho&speed=0&text="+str(sys.argv[1])+"' 'https://openapi.naver.com/v1/voice/tts.bin' -H 'Content-Type: application/x-www-form-urlencoded' -H 'X-Naver-Client-Id: wY8qYOdN9FzbBBrgtlF3' -H 'X-Naver-Client-Secret: _dblCskdHA' > unblock_completed.wav")
