# -*- coding: utf-8 -*-
import re

f=open("dominios.txt")
j=open("jose.txt")
joses=[]
for i in j.readlines():
	i=i.replace("\n","")		
	joses.append(i)


def check_jose(dominio):
	if  dominio in joses:
		#print dominio
		return True
	else:
		return False	

cnt=0
msg=""
for i in f.readlines():
	i=i.replace("\n","")
	i=i.split("\t")
	aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",i[4])
	#print i
	if aa:		
		if i[1]=="@":
			if check_jose(i[0]):
				msg= "\tMATCH"
				cnt+=1
			else:
				msg= "\t ***"
			
			print i[0] + msg
		else: 
			if check_jose(i[1]+"."+i[0]):
				msg= "\tMATCH"
				cnt+=1
			else:
				msg= "\t ***"
			
			#print i[1]+"."+i[0]	+ msg
		

print cnt