# coding=utf8

# 인증된 사용자가 "비밀번호 변경"이라고 말하면
# 라즈베리파이는 "비밀번호를 말하세요"라고 말한 후, 사용자가 비밀번호를 말하면 stt로 파싱하여 비밀번호가 전달됨. 그리고 이 파일이 수행된다.

# 2017.11.8 complete
import commands
import os
import sys
class Change_passwd:
	def change(self):
		bak="/etc/hostapd/hostapd.bak"
		origin="/etc/hostapd/hostapd.conf"
		
		# 백업파일 생성(비밀번호가 변경된 hostapd.conf 임시파일)
		os.system("sudo cp "+origin+" "+bak)
		
		# 이전 비밀번호 알아내기
		(status1,old_passwd)=commands.getstatusoutput("grep 'wpa_passphrase=' /etc/hostapd/hostapd.conf")
		if status1==0:
			# 새로운 스트링 변수에 wpa_passphrase=[newpassword]를 적용.
			new_passwd="wpa_passphrase="+sys.argv[1] # sys.argv[1]은 전달된 새로운 비밀번호
			
			# hostapd.conf파일에서 line_num행을 new_passwd로 대체함.
			os.system("sudo sed 's/"+old_passwd+"/"+new_passwd+"/' /etc/hostapd/hostapd.conf > chang_pass")
			os.system("sudo cp chang_pass "+origin)
			
			
if __name__=="__main__":
	try:
		if sys.argv[2]=="1":
			c_passwd=Change_passwd()
			c_passwd.change()
			os.system("sudo systemctl restart hostpad")
			os.system("omxplayer change_passwd_result.mp3")
			#os.system("sudo reboot")
	except:
		os.system("omxplayer please_admin.mp3")
		sys.exit(1)
