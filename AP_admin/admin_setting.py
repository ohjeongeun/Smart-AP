# coding=utf8
import os
import sys
import commands

# 사용자가 'admin설정할래 '이라고 말하면 이 파일이 수행된다.
# 라즈 : 답을 말하세요
# 사용자 : 1, 2, 3 
# 라즈 : (사용자가 말한 1,2,3이 정답파일에 있는 답 1,2,3과 같은지 비교한다. 파일을 불러와 리스트에 넣고 반복문 돌리기.) 
# 정답인 경우 라즈 : '정답입니다.' 하고 '무엇을 도와드릴까요?' 묻는다.
# 하나라도 오답인 경우 : '틀렸습니다.' 하고 파일 exit시켜버림.

# admin 설정 모드에 들어오면 비밀번호/ssid를 변경하거나, 나 이외 차단 기능을 설정할 수 있다.

class Admin_Setting():
	# 사용자 인증
	def admin_authen(self):
		flag=0
		
		ans=[] #사용자가 말한 답을 저장할 리스트
		
		for i in range(1,4):
			os.system("omxplayer Q_"+str(i)+".mp3") #질문
			
			# 여기서 음성인식 동작. 사용자는 답을 말한다. (파싱 하여 변수에 저장)
			os.system("rm -rf 3ao.wav")
			os.system("arecord -D 'plughw:1,0' -f S16_LE -t wav -r 16000 -d 4 > 3ao.wav")	
			os.system("curl -o stt_3ao.txt -X POST --data-binary @3ao.wav --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ko&key=AIzaSyC0SpDwgok-dLZrQtiAbdx1bA3p4_TCWNk'")
			os.system("sudo cat stt_3ao.txt | sed -n 2p | cut -d : -f4 | cut -d , -f1 | cut -d \\\" -f2 > stt_3ao2.txt")

			# ans[i-1]과 answers의 i번째 행이 같은지 판단.
			(status1,answer)=commands.getstatusoutput("sed -n "+str(i)+"p answers")
			(status2,ans)=commands.getstatusoutput("sed -n 1p stt_3ao2.txt")
			if status1==0:
				if ans==answer:
					#print(answer) 정답인 경우 
					flag=1
				else:
					os.system("omxplayer ttang.mp3") #오답인 경우 하나라도 오답으로 걸리면 프로그램 종료.
					flag=0
					sys.exit(1)
		return flag
		
	def admin_setting(self,set_flag):
		print(set_flag)
		os.system("omxplayer jungdab.mp3")
		
		# 여기에 음성인식 동작. 사용자는 1) "비밀번호/ssid를 변경" 혹은 2) "나 이외 차단"을 말할 수 있다.
		os.system("rm -rf 3ao.wav")
		os.system("arecord -D 'plughw:1,0' -f S16_LE -t wav -r 16000 -d 4 > 3ao.wav")
		os.system("curl -o stt_3ao.txt -X POST --data-binary @3ao.wav --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ko&key=AIzaSyC0SpDwgok-dLZrQtiAbdx1bA3p4_TCWNk'")
		os.system("sudo cat stt_3ao.txt | sed -n 2p | cut -d : -f4 | cut -d , -f1 | cut -d \\\" -f2 > stt_3ao2.txt")
		(status3,user_request)=commands.getstatusoutput("sed -n 1p stt_3ao2.txt")

		#user_request="비밀번호 변경" #음성인식 파싱 했을 때 값(예시)
		if "비밀번호 변경" in user_request or "비밀번호 변경해 줘" in user_request:
			print("비밀번호 변경")
			os.system("omxplayer tellme_newpw.mp3")
			#new_passwd="12312312"# 여기도 음성인식 동작. 사용자는 새로운 비밀번호를 말한다.
		
			os.system("rm -rf 3ao.wav")
                	os.system("arecord -D 'plughw:1,0' -f S16_LE -t wav -r 16000 -d 4 > 3ao.wav")
                	os.system("curl -o stt_3ao.txt -X POST --data-binary @3ao.wav --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ko&key=AIzaSyC0SpDwgok-dLZrQtiAbdx1bA3p4_TCWNk'")
                	os.system("sudo cat stt_3ao.txt | sed -n 2p | cut -d : -f4 | cut -d , -f1 | cut -d \\\" -f2 > stt_3ao2.txt")
                	(status4,new_passwd)=commands.getstatusoutput("sed -n 1p stt_3ao2.txt")
			new_passwd=new_passwd.strip().replace(" ","")
			os.system("python change_passwd.py "+str(new_passwd)+" "+str(set_flag))
		elif "ssid 변경" in user_request or "ssid 변경해 줘" in user_request:
			print("ssid 변경")
			os.system("omxplayer tellme_newsid.mp3")
			new_sid="3ao3ao"# 여기도 음성인식 동작. 사용자는 새로운 ssid를 말한다.
			new_sid=new_sid.strip().replace(" ","")
			os.system("python change_ssid.py "+str(new_sid)+" "+str(set_flag))
		elif "마이 왜 차단" in user_request or "마이 왜 차단해 줘" in user_request:
			print("나 이외 차단")
			os.system("cd ../AP_block;python block.py "+str(set_flag))
		elif "허용" in user_request or "풀어 줘" in user_request:
			print("허용")
			os.system("cd ../AP_block;python unblock.py "+str(set_flag))
		else:
			os.system("omxplayer wrong_request.mp3")


if __name__ =="__main__":
	set_flag=0
	admin_set=Admin_Setting()
	set_flag=admin_set.admin_authen()
	admin_set.admin_setting(set_flag)
