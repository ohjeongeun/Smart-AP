# coding=utf8

import os
import sys
import commands
class Unblock:
	def unblock_mac(self):
		print("unblock mac")
		(status1,my_address)=commands.getstatusoutput("cat ../AP_user/find_admin")
		os.system("sudo ufw delete allow from "+my_address)
		os.system("sudo ufw disable")
		os.system("omxplayer unblock_completed.wav")

if __name__=="__main__":
	try:
		if sys.argv[1]=="1":
			unblock=Unblock()
			unblock.unblock_mac()	
	except:
		print("권한이 없습니다.admin으로 로그인 하세요")
		os.system("omxplayer please_admin.mp3")
		sys.exit(1)
