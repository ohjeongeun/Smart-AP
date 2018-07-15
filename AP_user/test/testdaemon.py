# coding=utf8
import os 
import sys
import commands
import time
class Daemon:
	def check_line(self): 
		f=open("user.log","w")
		(line_status, lines)=commands.getstatusoutput("cat test.log|wc -l")
		while(1):
			(line_status2, lines2)=commands.getstatusoutput("cat test.log|wc -l")
			if int(lines)<int(lines2):
				print('different')
				line_num=int(lines2)-int(lines) #추가된 라인 수
				(status,result)=commands.getstatusoutput("tail -"+str(line_num)+" test.log | grep -w 'DHCPACK\|IEEE 802.11: disassociated'")
				f.write(result)
				lines=lines2
			time.sleep(1)
		f.close()
			
if __name__ == "__main__":
	d=Daemon()
	d.check_line()
