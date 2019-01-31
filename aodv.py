from socket import *
import subprocess, sys, shlex
import threading
import time
import json
import csv
	
packet_type = ["RREQ", "RREP", "RERR"]
hosts = ["Dawood","Emma","Faryal","Gul","Ahmed","Bilal","Charlie"]

RREQ_packet = {"src_address": "0", "src_seq": 0, "broadcast_id": 0,"dest_address": "0", "dest_seq": 0, "hop_count": 0}
RREP_packet = {"src_address": "0","dest_address": "0", "dest_seq": 0, "hop_count": 0, "lifetime": 0}

myDictionary = {'Charlie':'10.92.255.0', 'Dawood':'10.92.255.1', 'Emma':'10.92.255.2', 'Faryal':'10.92.255.3', 'Gul':'10.92.255.4', 'Ahmed':'10.92.255.5', 'Bilal':'10.92.255.6' }
inverse = {'10.92.255.0':'Charlie', '10.92.255.1':'Dawood', '10.92.255.2':'Emma', '10.92.255.3':'Faryal', '10.92.255.4':'Gul', '10.92.255.5':'Ahmed', '10.92.255.6':'Bilal'}

Llock = 1
port = 8001
hosts = ['10.92.255.0', '10.92.255.1', '10.92.255.2', '10.92.255.3', '10.92.255.4', '10.92.255.5', '10.92.255.6']

def CreateTopology():
	
	for i in range(1,8):
		f = open(hosts[i]+".txt", "w")
		
		f.write(host_ip[i])		
		
		if i == 1:   
			f.write("\nNeighbors: " + hosts[7] + "," + hosts[i+1])

		elif i == 7:
			f.write("\nNeighbors: " + hosts[i-1] + "," + hosts[1])
		
		else:
			f.write("\nNeighbors: " + hosts[i-1] + "," + hosts[i+1])
		
		cmd = "x-terminal-emulator -e 'sudo python3.4 /home/nabeel31333/CN-project/node.py " + hosts[i] + "'"
		process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
	
def listen(host, port):
	global Llock
	#time.sleep(1)
	s = socket(AF_INET,SOCK_DGRAM)

	try:
		s.bind((host, port))
	except error as msg:
		print 'error here'
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message: ' + str(msg[1])
		s.close()
		sys.exit()
	
	while True:
		if Llock == 1:
			Llock = 0		
			while True:	    
				print '\nSocket now listening at ', host	
				Llock = 1			
				message, cAddress = s.recvfrom(2048)
				print message
				data_loaded = json.loads(message) #data loaded
				
				dump = {"dest": data_loaded['source'], "next":data_loaded['from'], "seq":data_loaded['seq#'], "hop_count":data_loaded['hop_count']}
				path = inverse[host] + ".txt"
				with open(path,'w') as txtFile:
					txtFile.write(str(dump["dest"]) +","+ str(dump["next"])+","+str(dump["seq"])+","+str(dump["hop_count"]))
					txtFile.write('\n')									
				print "\nReceived at ", cAddress
				modifiedMessage = "\nReceived at " + str(host)
				s.sendto(modifiedMessage, cAddress)
			s.close()
			time.sleep(3)	

def createThreads():
	
	t1 = threading.Thread(target=listen, args = (hosts[0],port)) #node 1
		
	t3 = threading.Thread(target=listen, args = (hosts[1],port)) #node 2

	t5 = threading.Thread(target=listen, args = (hosts[2],port)) #node 3

	t7 = threading.Thread(target=listen, args = (hosts[3],port)) #node 4

	t9 = threading.Thread(target=listen, args = (hosts[4],port)) #node 5

	t11 = threading.Thread(target=listen, args = (hosts[5],port)) #node 6

	t13 = threading.Thread(target=listen, args = (hosts[6],port)) #node 7
	
	startListeners(t1,t3,t5,t7,t9,t11,t13)

def startListeners(t1,t3,t5,t7,t9,t11,t13):
	
	try:
		t1.start()
		t3.start()
		t5.start()
		t7.start()
		t9.start()
		t11.start()
		t13.start()
	except:
		print "Unable to start threads"

#CreateTopology()
#main()

createThreads()
