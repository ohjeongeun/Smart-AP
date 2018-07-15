# coding=utf8
import os 
import sys
import commands
import time


# 라즈베리파이가 켜지면 자동으로 돌아가는 데몬. 공유기 접속자의 출입을 모니터링 하여 user.log를 만든다. 
# user.log는 DHCP를 할당받거나 disassociated한 기록이 담겨 있다.

# 2017.10.30 complete
class Daemon:
	def check_line(self): 
		if os.path.isfile("user.log") or os.path.isfile("find_admin"):
			os.system("sudo rm ./user.log")
			os.system("sudo rm ./find_admin")
		(line_status, lines)=commands.getstatusoutput("cat /var/log/daemon.log|wc -l")
		while(1):
			(line_status2, lines2)=commands.getstatusoutput("cat /var/log/daemon.log|wc -l")
			if int(lines)<int(lines2):
				print('different')
				line_num=int(lines2)-int(lines) #추가된 라인 수
				os.system("tail -"+str(line_num)+" /var/log/daemon.log | grep -w 'DHCPACK\|IEEE 802.11: disassociated' >> ./user.log")
				lines=lines2
			time.sleep(1)
			
if __name__ == "__main__":
	d=Daemon()
	d.check_line()
