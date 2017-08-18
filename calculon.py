# -*- coding: utf-8 -*-
import string
import random
import sqlite3 as lite
import sys
import os
from xlsxwriter.workbook import Workbook
from colorama import init, Fore, Back, Style
init()

con = lite.connect('codes.db')
longcode = 6
typecode = string.ascii_uppercase + string.digits
quantitycode = 100
formatcode = 'xlsx'

def main():
	banner()
	longoption()

def clear():
	os.system('cls')

def banner():
	clear()
	print(Fore.GREEN + '''
		  ,     ,
	         (\____/)
	          (_oo_)
	            (O)
	          __||__    \)
	       []/______\[] /
	       / \______/ \/
	      /    /__\                                                                          
	     (\   /____\                                                                         
                                                                                             
		 .d8888b.        d8888 888      .d8888b.  888     888 888      .d88888b.  888b    888 
		d88P  Y88b      d88888 888     d88P  Y88b 888     888 888     d88P" "Y88b 8888b   888 
		888    888     d88P888 888     888    888 888     888 888     888     888 88888b  888 
		888           d88P 888 888     888        888     888 888     888     888 888Y88b 888 
		888          d88P  888 888     888        888     888 888     888     888 888 Y88b888 
		888    888  d88P   888 888     888    888 888     888 888     888     888 888  Y88888 
		Y88b  d88P d8888888888 888     Y88b  d88P Y88b. .d88P 888     Y88b. .d88P 888   Y8888 
		 "Y8888P" d88P     888 88888888 "Y8888P"   "Y88888P"  88888888 "Y88888P"  888    Y888 

		 By EzeSoler                                                                    v 1.0
		''')

def longoption():
	global longcode
	print(Fore.YELLOW +'''
		\n
		Generador de codigos aleatorios y unicos.
		Ingrese el numero de logitud que debera tener el codigo (Ej. 6)
		''')
	try:
		longcode = int(raw_input(Fore.YELLOW +'''
		Longitud codigo: 
		'''))
	except ValueError:
		clear()
		print(Fore.WHITE + Back.RED +'''
		El valor ingresado debe ser numerico.
		''')
		print(Style.RESET_ALL)
		longoption()
	else:
		clear()
		typeopcion()

def typeopcion():
	global typecode
	print(Fore.YELLOW +'''
		\n
		Seleccione el tipo de codigo:
		\n
		1 - Alfanumerico
		2 - Alfabetico
		3 - Numerico
		''')
	choice = raw_input(Fore.YELLOW +'''
		Ingrese opcion: 
		''')
	if choice == '1':
		typecode = string.ascii_uppercase + string.digits
		clear()
		quantityoption()
	if choice == '2':
		typecode = string.ascii_uppercase
		clear()
		quantityoption()
	if choice == '3':
		typecode = string.digits
		clear()
		quantityoption()
	else:
		clear()
		print(Fore.WHITE + Back.RED +'''
		Esa no es una opcion papu!.
		''')
		print(Style.RESET_ALL)
		typeopcion()

def quantityoption():
	global quantitycode
	print(Fore.YELLOW +'''
		\n
		Ingrese la cantidad de codigos que desea generar.
		\n
		''')
	try:
		quantitycode = int(raw_input(Fore.YELLOW +'''
		Cantidad de codigos: 
		'''))
	except ValueError:
		clear()
		print(Fore.WHITE + Back.RED +'''
		El valor ingresado debe ser numerico... no es tan dificil
		''')
		print(Style.RESET_ALL)
		quantityoption()
	else:
		clear()
		exportoption()

def exportoption():
	global formatcode
	print(Fore.YELLOW +'''
		\n
		Seleccione el tipo de formato de exportacion:
		\n
		1 - Excel
		2 - Texto Plano
		''')
	choice = raw_input(Fore.YELLOW +'''
		Ingrese opcion: 
		''')
	if choice == '1':
		formatcode = 'xlsx'
		clear()
		generatecodes()
	if choice == '2':
		formatcode = 'txt'
		clear()
		generatecodes()
	else:
		clear()
		print(Fore.WHITE + Back.RED +'''
		Esa no es una opcion papu!.
		''')
		print(Style.RESET_ALL)
		exportoption()

def resettable():
	try:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Codes;")
		cur.execute("CREATE TABLE codes(code TEXT)")
		con.commit()
	except lite.Error, e:
		print "Error %s:" % e.args[0]
    	#sys.exit(1)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def checkcode(c):
	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM codes WHERE code = '%s'" % c)
		result = cur.fetchone()
		if result is None:
			return False
		else:
			return True
	except lite.Error, e:
		print "Error %s:" % e.args[0]
    	#sys.exit(1)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '|'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r\t\t%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total: 
        print "\n"

def generatecodes():
	resettable()
	print(Fore.GREEN +'''
		Generando codigos...
		''')
	count = 0
	printProgressBar(0, quantitycode, prefix = 'Progreso:', suffix = 'Completado', length = 50)
	while (count < quantitycode):
		try:
			code = id_generator(int(longcode),typecode)
			printProgressBar(count, quantitycode, prefix = 'Progreso:', suffix = 'Completado', length = 50)
			#sys.stdout.write("""\r%d%%""" % count)
			#sys.stdout.flush()
			if not checkcode(code):
				cur = con.cursor()
				cur.execute("INSERT INTO codes (code) VALUES (?);",[code])
				con.commit()
				count += 1
		except lite.Error, e:
			print "Error %s:" % e.args[0]
    		#sys.exit(1)
	clear()
	exportcodes()

def exportcodes():
	print(Fore.GREEN +'''
		Exportando codigos...
		''')
	filename = "codes_%s" % random.randint(100, 999)
	if formatcode == "xlsx":
		workbook = Workbook("%s.xlsx" % filename)
		worksheet = workbook.add_worksheet()
	else:
		textfile = open("%s.txt" % filename, "w")
	cur = con.cursor()
	result = cur.execute("SELECT code FROM codes")
	codes = result.fetchall()
	rows = 0;
	for row in codes:
		if formatcode == "xlsx":
			worksheet.write(rows, 0, row[0])
		else:
			textfile.write("%s\n" % row[0])
		rows += 1
	if formatcode == "xlsx":
		workbook.close()
	else:
		textfile.close()
	clear()
	print(Fore.GREEN + '''
		  ,     ,
	         (\____/)
	          (_oo_)
	            (O)
	          __||__    \)
	       []/______\[] /
	       / \______/ \/
	      /    /__\                                                                          
	     (\   /____\   ''')
	print(Fore.YELLOW +'''
		El archivo %s.%s se ha exportado correctamente ;)
		''' % (filename,formatcode))
	sys.exit()

main()