# coding=utf8
import os
import sys
import commands
import time
import random

# 부팅 시 맨 처음 자동으로 수행되는 스크립트.
# 3개의 질문을 0.6초의 텀을 두고 랜덤으로 연속해서 던진다.(그러면 사용자는 답 3개를 연속하여 말한다.)
# 사용자가 답한 것을 파일로 저장한다. 

# 2017.11.10 tts complete

class Login:
	def admin_login(self):
		# random number
		question_number=random.sample(range(1,40),3)
		
		# ask to user
		question_list=[]
		for i in question_number:
			(status1,question)=commands.getstatusoutput("sed -n "+str(i)+"p questions")
			if status1==0:
				question_list.append(question)
		num=1
		for question in question_list:
			# 음원 재생(질문)
			os.system("curl -d 'speaker=jinho&speed=0&text="+question+"' 'https://openapi.naver.com/v1/voice/tts.bin' -H 'Content-Type: application/x-www-form-urlencoded' -H 'X-Naver-Client-Id: wY8qYOdN9FzbBBrgtlF3' -H 'X-Naver-Client-Secret: _dblCskdHA' > Q_"+str(num)+".mp3")
			os.system("omxplayer Q_"+str(num)+".mp3")
			num=num+1
			# 여기서 음성인식 시작. (답)
			os.system("rm -rf 3ao.wav")
			os.system("arecord -D 'plughw:1,0' -f S16_LE -t wav -r 16000 -d 4 > 3ao.wav")
			os.system("curl -o 3ao_login.txt -X POST --data-binary @3ao.wav --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ko&key=AIzaSyC0SpDwgok-dLZrQtiAbdx1bA3p4_TCWNk'")
			# answers파일에 붙이기
			os.system("cat 3ao_login.txt | sed -n 2p | cut -d : -f4 | cut -d , -f1 | cut -d \\\" -f2 >> answers")
			time.sleep(0.6)



if __name__ == "__main__":
	login=Login()
	login.admin_login()
	os.system("omxplayer admin_login_result.mp3")
