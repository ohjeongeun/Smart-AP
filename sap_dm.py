# coding=utf8
import os
import sys
import commands
import time
sys.path.append("/home/pi/Capston-Design-3AO/stt")
import stt_complete

# 공유기 시작시 켜지는 데몬. 
# 이 데몬이 동작하면 sap은 음성인식 공유기로서 기능읗 한다.(사용자의 말 listen)
# 음성인식은 5초에 한 번 씩 다시 시작한다.
class SAP:
	def sap_dm(self):
		KEY_CONST1="어드민"
		KEY_CONST2="사용자"
		KEY_CONST3="시작"
		KEY_CONST4="비밀번호"
		KEY_CONST5="ssid"
		KEY_CONST6="차단"
		KEY_CONST7="허용"
		KEY_CONST8="풀어 줘"
		os.system("omxplayer start.wav")
		while(1):
			print("SAP_daemon...")
			stt_complete.STT()
			time.sleep(1)
			(status1,cmd)=commands.getstatusoutput("cat stt_3ao2.txt")
			if KEY_CONST1 in cmd:
				print("어드민")
				os.system("cd AP_admin;python admin_setting.py") 
			elif KEY_CONST2 in cmd:
				print("사용자")
				os.system("cd AP_user;python ap_num.py")
			elif KEY_CONST3 in cmd:
				print("시작")
				os.system("cd AP_restart;python restart.py")
			elif KEY_CONST4 in cmd or KEY_CONST5 in cmd:
				os.system("권한이 없습니다. 어드민으로 로그인하세요")
				os.system("cd AP_admin;omxplayer please_admin.mp3")
			elif KEY_CONST6 in cmd:
				os.system("권한이 없습니다. 어드민으로 로그인하세요")
				os.system("cd AP_admin;omxplayer please_admin.mp3")
			elif KEY_CONST7 in cmd or KEY_CONST8 in cmd:
				os.system("권한이 없습니다. 어드민으로 로그인하세요")
				os.system("cd AP_admin;omxplayer please_admin.mp3")
			else:
				print("이해하지 못했습니다.")
				#os.system("omxplayer notmyway.wav")
		

if __name__=="__main__":
	sap=SAP()
	sap.sap_dm()
