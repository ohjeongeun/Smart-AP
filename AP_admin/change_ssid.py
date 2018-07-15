# coding=utf8

# change_passwd.py와 같은 방법. ssid를 변경해 준다.

# 2017.11.8 complete
import commands
import os
import sys
class Change_ssid:
	def change(self):
		bak="/etc/hostapd/hostapd.bak"
		origin="/etc/hostapd/hostapd.conf"
		
		os.system("sudo cp "+origin+" "+bak)
		
		# 이전 비밀번호 알아내기
		(status1,old_ssid)=commands.getstatusoutput("grep 'ssid=' /etc/hostapd/hostapd.conf | head -1")
		if status1==0:
			# 새로운 스트링 변수에 ssid=[newssid]를 적용.
			new_ssid="ssid="+sys.argv[1] # sys.argv[1]은 전달된 새로운 ssid
			
			# hostapd.conf파일에서 old_ssid행을 new_ssid로 대체함.
			os.system("sudo sed 's/"+old_ssid+"/"+new_ssid+"/' /etc/hostapd/hostapd.conf > chang_ssid")
			os.system("sudo cp chang_ssid "+origin)
			
			
if __name__=="__main__":
	try:
		if sys.argv[2]=="1":
			c_ssid=Change_ssid()
			c_ssid.change()
			os.system("sudo systemctl restart hostapd")
			os.system("omxplayer change_passwd_result.mp3")
			#os.system("sudo reboot")
	except:
		os.system("omxplayer please_admin.mp3")
		sys.exit(1)
