# coding=utf8
import re
import os
import sys
import commands

# 사용자 수를 구하는 클래스이다.
# 사용자가 '사용자 수가 뭐야?'라는 질문을 던지면 이 파일이 실행된다.
class UserNum:
        # 밑에서 부터 DHCPACK를 찾으면 해당 행을 공백으로 쪼개서 리스트로 만든다.
        def make_dhcp_list(self):
                dhcpack_list=[]
                (line_status,lines)=commands.getstatusoutput("cat user.log | wc -l") #user.log의 라인 수
                for line in range(int(lines),0,-1): # 끝에서 부터 돌면서 dhcp_list와 dis_list에 들어갈 애들을 나누어 담는다.
                        (dhcp_status,dhcpack)=commands.getstatusoutput("cat user.log | sed -n "+str(line)+"p")
                        dhcp_ack=re.split(" ",dhcpack)
                        if 'DHCPACK' in dhcp_ack[5]:
                                dhcpack_list.append(dhcp_ack)
                return dhcpack_list


        def make_real_userlist(self, dhcpack_list):
                # i, j(i+1)번째의 dhcpack_list[5]를 비교하고, 같으면 j번째 데이터를 지우고, dhcpack_list를 정정한다.
		# dhcpack_list는 user.log에서 중복을 제거한 최근에 공유기에 접속한 사용자 리스트.
                for i in range(0,len(dhcpack_list)-1):
                        for j in range(i+1,len(dhcpack_list)):
                                if dhcpack_list[i][7]==dhcpack_list[j][7]:
                                        del dhcpack_list[j]

		# dhcpack_list를 돌면서 user.log에서 라인을 찾는다. 
		# 그 라인 이후에 나타나는 맥주소가 같은 disassociated가 있다면 해당 행을 삭제한다.
		# 최종 user.log는 사용자 리스트가 된다.
		for i in range(0,len(dhcpack_list)):
			dhcp_time=dhcpack_list[i][0]+" "+dhcpack_list[i][1]+" "+dhcpack_list[i][2]
			dhcp_dhcp=dhcpack_list[i][5]
			dhcp_mac=dhcpack_list[i][7]
			(status,find_dhcp)=commands.getstatusoutput("grep -wn '"+dhcp_time+"' user.log | grep -w '"+dhcp_dhcp+"' | grep -w '"+dhcp_mac+"'")

			if status==0:
				dhcp_number=find_dhcp[0]
				(status2, lines)=commands.getstatusoutput("cat user.log | wc -l")
				for line in range(int(lines),int(dhcp_number),-1):
					(status3, dis_asso)=commands.getstatusoutput("cat user.log | sed -n "+str(line)+"p | grep -w 'disassociated' | grep -w '"+dhcp_mac+"'")
					if dis_asso:
						# dis_asso가 발견되었으므로 맥주소가 dhcp_mac인  dhcpack_list의 원소를 삭제한다.
						for i in range(0,len(dhcpack_list)):
							if dhcpack_list[i][7]==dhcp_mac:
								del dhcpack_list[i]
		return len(dhcpack_list)


if __name__=="__main__":
        dhcpack_list=[]
	user_account=0
        un=UserNum()
        dhcpack_list=un.make_dhcp_list()
        user_account=un.make_real_userlist(dhcpack_list)
	print(user_account)

