import os
import sys

def STT():
	os.system("rm -rf 3ao.wav")
	os.system("arecord -D 'plughw:1,0' -f S16_LE -t wav -r 16000 -d 4 > 3ao.wav")
	os.system("curl -o stt_3ao.txt -X POST --data-binary @3ao.wav --header 'Content-Type: audio/l16; rate=16000;' 'https://www.google.com/speech-api/v2/recognize?output=json&lang=ko&key=AIzaSyC0SpDwgok-dLZrQtiAbdx1bA3p4_TCWNk'")
	os.system("sudo cat stt_3ao.txt | sed -n 2p | cut -d : -f4 | cut -d , -f1 | cut -d \\\" -f2 > stt_3ao2.txt")

STT()
