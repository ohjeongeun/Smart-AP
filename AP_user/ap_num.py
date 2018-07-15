# coding=utf8
import re
import os
import sys
import commands

# 사용자 수를 구하는 클래스이다.
# 사용자가 '사용자 수가 뭐야?'라는 질문을 던지면 이 파일이 실행된다.

# 2017.11.2 complete
class UserNum:
        # user.log 파일의 끝 부터 DHCPACK를 찾으면 해당 행을 공백으로 쪼개서 리스트로 만든다.(맥주소 접근 용이)
	# 중복을 제거하여 리턴한다.
        def make_dhcp_list(self):
                dhcpack_list=[]
		DHCPACK_list=[]
                (line_status,lines)=commands.getstatusoutput("cat user.log | wc -l") #user.log의 라인 수
                for line in range(int(lines),0,-1):
                        (dhcp_status,dhcpack)=commands.getstatusoutput("cat user.log | sed -n "+str(line)+"p")
                        dhcp_ack=re.split(" ",dhcpack)
                        if 'DHCPACK' in dhcp_ack[6]:
                                dhcpack_list.append(dhcp_ack)

                # i, j(i+1)번째의 dhcpack_list[7](맥주소)를 비교하고, 같으면 j번째 데이터를 지우고, dhcpack_list를 정정한다.
		# dhcpack_list는 user.log에서 중복을 제거한 최근에 공유기에 접속한 사용자 리스트.
		len_dhcpack=len(dhcpack_list)
		for i in range(0,len_dhcpack-1): # 길이가 4인 경우 3번 반복.(0,1,2)
			for j in range(i+1,len_dhcpack): # 길이 4인 경우 0->1,2,3 / 1->2,3 / 2->3
				if dhcpack_list[i][8]==dhcpack_list[j][8]:
					dhcpack_list[j][8]="delete"

		DHCPACK_list=[]
		for k in range(0,len_dhcpack):
			if "delete" not in dhcpack_list[k][8]:
				DHCPACK_list.append(dhcpack_list[k][7])
				
                return DHCPACK_list


        def make_real_userlist(self, dhcpack_list):
		# dhcpack_list를 돌면서 user.log에서 라인을 찾는다. 
		# 그 라인 이후에 나타나는 맥주소가 같은 disassociated가 있다면 dhcpack_list원소를 삭제한다.(접속 했다가 공유기 접속을 끊은 사용자)
		# 최종 dhcpack_list는 사용자 리스트가 된다.
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
		return dhcpack_list,len(dhcpack_list)
	

	def find_admin(self,user_ack):
		for i in range(0,len(user_ack)):
			join_str="".join(user_ack[i])
			os.system("echo '"+join_str+"' > find_admin")


if __name__=="__main__":
        dhcpack_list=[]
	user_ack=[]
	user_account=0
        un=UserNum()
        dhcpack_list=un.make_dhcp_list()
        user_ack,user_account=un.make_real_userlist(dhcpack_list)
	un.find_admin(user_ack)

	os.system("curl -d 'speaker=jinho&speed=0&text=공유기 사용 인원은 "+str(user_account)+"명 입니다.' 'https://openapi.naver.com/v1/voice/tts.bin' -H 'Content-Type: application/x-www-form-urlencoded' -H 'X-Naver-Client-Id: wY8qYOdN9FzbBBrgtlF3' -H 'X-Naver-Client-Secret: _dblCskdHA' > ap_num.mp3")
	print(user_account)
	#os.system("omxplayer ap_num.mp3")

