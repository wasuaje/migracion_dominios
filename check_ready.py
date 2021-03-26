#!/usr/bin/python
# -*- coding: utf-8 -*-

from prettytable import PrettyTable
import sys
import dns.resolver
import itertools
import threading
import time
import argparse

class check_ready:
	def animate(self):
		
		#print dir(data)
		for c in itertools.cycle(['|', '/', '-', '\\']):
			if self.done:
				break
			try:
				sys.stdout.write('\rProcesando . . . Espere  ' +  c)
			except AttributeError as e: 
				print "Error ",e

			sys.stdout.flush()
			time.sleep(0.1)
		sys.stdout.write('\rDone!     ')


	def main_process(self):
		tbl = PrettyTable(["Registro", "Ip GOOGLE", "Ip DNS LOCAL", "Dif."])

		resol_google = dns.resolver.Resolver()
		resol_google.nameservers = ['8.8.8.8']
		resol_local = dns.resolver.Resolver()
		resol_local.nameservers = ['10.1.3.253']
		#print answer.rrset.items[0]
		#para pruebas
		#f=open("dom.txt")
		f=open("dominios.txt")

		self.done = False
		t = threading.Thread(target=self.animate)
		t.start()

		for i in f.readlines():
			err_g=False
			err_l=False	
			#print dir(t)
			i=i.replace("\n","")
			i=i.split("\t")	
			if len(i)>1:
				if i[1]=="@":
					host=i[0]
				else:
					host=i[1]+"."+i[0]
			else:
				host=i[0]
								
			try:
				output_g = resol_google.query(host)		
			except :
				#print host,"Error GOOGLE"				
				try:
					output_l = resol_local.query(host)
				except:
					#print i,"Error LOCAL"			
					tbl.add_row([host,"NO SE ENCONTRO","NO SE ENCONTRO"," "])
				else:
					tbl.add_row([host,"NO SE ENCONTRO",output_l.rrset.items[0]]," *** ")
			else:
				try:
					output_l = resol_local.query(host)
				except:
					#print i,"Error LOCAL"			
					tbl.add_row([host,output_g.rrset.items[0],"NO SE ENCONTRO", " *** "])
				else:
					if output_g.rrset.items[0] == output_l.rrset.items[0]:
						if self.opt.full:
							tbl.add_row([host,output_g.rrset.items[0],output_l.rrset.items[0]," "])	
					else:
						tbl.add_row([host,output_g.rrset.items[0],output_l.rrset.items[0]," *** "])	

		self.done = True		

		print "\n"
		print tbl

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Lista dominios con DNS google y local")
	
	parser.add_argument('-f', '--full', action='store_true',
					dest='full',
					help='Lista completa de dominios señalando diferencias'   )
	parser.add_argument('-d', '--diff', action='store_true',
					dest='diff',
					help='Lista solo los dominios con diferencias'   )	
	
	args = parser.parse_args()	

	if args.full or args.diff	:	
		ch=check_ready()
		ch.opt=args
		ch.main_process()
		#main_process(args)
	else:		
		print parser.print_help()
