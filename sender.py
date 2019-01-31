from socket import *
import threading
import json

Slock = 1
port = 8001
hosts = ['10.92.255.0', '10.92.255.1', '10.92.255.2', '10.92.255.3']

Routes = {	"Charlie":["Dawood", "Bilal"], 
			"Dawood":["Emma", "Charlie"], 
			"Emma":["Faryal", "Dawood"], 
			"Faryal":["Gul", "Emma"],
			"Gul":["Ahmed", "Faryal"],
			"Ahmed":["Bilal", "Gul"],
			"Bilal":["Charlie", "Ahmed"],
			}

clockWiseRoutes = ["Dawood", "Emma", "Faryal", "Gul", "Ahmed", "Bilal", "Charlie"]
anticlockWiseRoutes = ["Dawood", "Charlie", "Bilal", "Ahmed", "Gul", "Faryal", "Emma"]			

myDictionary = {'Charlie':'10.92.255.0', 'Dawood':'10.92.255.1', 'Emma':'10.92.255.2', 'Faryal':'10.92.255.3', 'Gul':'10.92.255.4', 'Ahmed':'10.92.255.5', 'Bilal':'10.92.255.6' }

def send(host, port, pkt):
	global Slock
	data_string = json.dumps(pkt) #data serialized

	while True:
		if Slock == 1:
			Slock = 0
			s = socket(AF_INET,SOCK_DGRAM)    
			s.sendto(data_string,(host,port))
			message, serverAddress = s.recvfrom(2048)
			print message
			s.close()
			Slock = 1	
			break


def createPacket(src,seq,dest,hop,pktType, curr):
	pkt = {"source":src, "seq#":seq,"destination":dest, "hop_count":hop, "Packet_Type":pktType, "from": curr}
	return pkt
	
while 1:
	y = raw_input("\nWho are you? ")
	solid_source = y
	x =  raw_input("\nWho do you want to send a message to? ")
	solid_dest = x
	temp = y
	hop = 0
	seqS = 100
	ind1 = clockWiseRoutes.index(y)
	ind2 = clockWiseRoutes.index(x)
	result1 = abs(ind2-ind1)

	ind1 = anticlockWiseRoutes.index(y)
	ind2 = anticlockWiseRoutes.index(x)
	result2 = abs(ind2-ind1)

	if result1 > result2:
		select = anticlockWiseRoutes
	elif result1 < result2:
		select = clockWiseRoutes
	else:
		select = clockWiseRoutes

	sourceIndex = select.index(y)
	destIndex = select.index(x)
	print destIndex
	for i in range(sourceIndex+1, destIndex+1):
	#while temp != x:                      #Route Request (RREQ)
		#if x and y in myDictionary:
			#if y in Routes:
				#neighbors = Routes[y]    #get neighbors of y
				next = select[i]		#get first neighbor from list of neighbors
				pktType = "RREQ"		
				pkt = createPacket(solid_source,seqS,solid_dest,hop,pktType,y)
				hop += 1
				y = next                #now our current is first neighbor
				#sender_ip = myDictionary[y]
				ip = myDictionary[next]	
				send(ip,port,pkt)

	hop = 0
	seqR = 120
	for i in range(destIndex-1, sourceIndex-1, -1):
	#while temp != solid_source:			#Route Reply (RREP)
		pktType = "RREP"
		next = select[i]		
		pkt = createPacket(solid_dest, seqR, solid_source,hop,pktType,temp)
		ip = myDictionary[next]
		send(ip, port, pkt)
		temp = next
		hop += 1