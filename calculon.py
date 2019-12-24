#!/usr/bin/env python3

import sqlite3 as lite
import sys
import signal

from os import (
                    system,
                    name as whoami)
from secrets import (
                        token_hex,
                        token_urlsafe)  # Creeme, es mucho mejor ;)
from random import choice as array_random
from xlsxwriter.workbook import Workbook
from colorama import init, Fore, Back, Style

init()

class config(object):
    choice = None
    con = lite.connect('codes.db')
    quantitycode = None
    formatcode = {

            '1': 'xlsx',
            '2': 'txt'

    }
    humor = [
                'No deberia ejecutar esa opción por su propio bien...',
                '¡Tenga cuidado!',
                'Si vuelve a ejecutar una opción incorrecta, su máquina explota',
                'Esta no es una opción papu!',
                    '¡No vuelva a equivocarse!',
                'Creo que su sistema operativo tiene un virus, borre'
                '"C:\\Windows\\System32" para arreglarlo',
                'Creo que este programa es un virus... Jaja, es broma... o tal vez '
                'no... 3:)']

def _input(prompt=''):
    while (True):
        try:
            return(input(prompt))

        except EOFError:
            continue

        else:
            break

def protect(signum, frame):
    print(Fore.GREEN, "Gracias :D ...", Style.RESET_ALL)
    sys.exit(1)

def clear():
    if (whoami == 'nt'):
        system('cls')

    else:
        # Es mejor usar los códigos ANSI porque mejora el rendimiento.
        print('\033[1f\033[2J', end='')
                                        # Aunque sólo funciona para los SO
                                        # Posix.

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

             By EzeSoler                                                                    v 2.0
            ''')

def _join_to_string(*args):
    return(''.join(args))

def longoption():
    while (True):

        print(
                Fore.YELLOW, '\n',
                '\n', 'Generador de codigos aleatorios y unicos.',
                '\n', 'Ingrese el numero de logitud que debera tener el codigo (Ej. 6)')
        try:

            config.longcode = _input(_join_to_string(
                Fore.YELLOW,
                '\n', 'Longitud del código:', '\n'))

            if (config.longcode.strip() == ''):

                print('\n', '¡Debe ingresar un valor!', '\n')
                continue

            else:

                config.longcode = int(config.longcode)

        except ValueError:
            clear()

            print(
                    '\n', Fore.WHITE,
                    Back.RED, 'El valor ingresado debe ser numerico.', Style.RESET_ALL, '\n')

        else:
            break

    clear()
    typeopcion()

def typeopcion():
    while (True):
        print(
                Fore.YELLOW,
                '\n', 'Seleccione el tipo de código:',
                '\n', '1 - Alfanumerico',
                '\n', '2 - Numerico', '\n')
        config.choice = _input(_join_to_string(
                                        Fore.YELLOW,
                                        '\n', 'Ingrese una opción:', '\n'))[:1]
        clear()
        if not (config.choice in ['1', '2']):
            print(
                    '\n', Fore.WHITE,
                    Back.RED, array_random(config.humor), Style.RESET_ALL, '\n')

        else:
            break

    quantityoption()

def quantityoption():
    while (True):
        print(Fore.YELLOW,
                '\n', 'Ingrese la cantidad de códigos que desea generar.', '\n')
        try:

            config.quantitycode = _input(_join_to_string(Fore.YELLOW, '\n' 'Cantidad de códigos:' '\n'))
            if (config.quantitycode.strip() == ''):
                print()
            config.quantitycode = int(config.quantitycode)

        except ValueError:
            clear()
            
            print(
                    '\n', Fore.WHITE,
                    Back.RED, 'El valor ingresado debe ser numerico... oh vamos, no es tan dificil', Style.RESET_ALL, '\n')

        else:
            break
    clear()
    exportoption()

def exportoption():
    while (True):
        print(Fore.YELLOW,
                '\n', 'Seleccione el tipo de formato de exportación:',
                '\n', '1 - Excel',
                '\n', '2 - Texto Plano', '\n')

        try:
            config.formatcode=config.formatcode[_input(Fore.YELLOW + '\n' 'Ingrese una opción:' '\n')]

        except KeyError:
            clear()

            print(
                    '\n', Fore.WHITE,
                    Back.RED, array_random(config.humor), Style.RESET_ALL, '\n')

        else:
            break

    generatecodes()

def resettable():
    try:
        cur=config.con.cursor()
        cur.execute("DROP TABLE IF EXISTS Codes;")
        cur.execute("CREATE TABLE codes(code TEXT)")
        config.con.commit()
    except lite.Error as e:
        print('Error {}:'.format(e.args[0]))

def id_generator(size=64):
    try:
        token = token_hex(size)

    except OverflowError:
        print(
                Fore.WHITE, Fore.RED,
                '\n', "La longitud de los códigos es muy larga :/ ...", '\n',
                Style.RESET_ALL)
        sys.exit(1)

    else:
        return(token if (config.choice == '1') else str(int(token, 16)))

def checkcode(c):
    try:
        cur=con.cursor()
        cur.execute("SELECT * FROM codes WHERE code = '%s'" % c)
        result=cur.fetchone()
        
        if result is None:
            return(False)
        else:
            return(True)

    except lite.Error as e:
        print('Error {}:'.format(e.args[0]))

def generatecodes():
    resettable()

    print(Fore.GREEN,
            '\n', 'Generando códigos...', '\n')
    
    for _ in range(config.quantitycode):
    
        try:
            cur=config.con.cursor()
            cur.execute("INSERT INTO codes (code) VALUES (?);", [id_generator(config.longcode)])
            config.con.commit()

        except lite.Error as e:
            print('Error %s:' % e.args[0])

    clear()
    exportcodes()

def exportcodes():
    print(Fore.GREEN, '\n', 'Exportando códigos...', '\n')

    filename="codes_%s" % (token_urlsafe(5))  # 10 elementos, recuerda n*2
    
    with Workbook('{}.xlsx'.format(filename)) \
            if (config.formatcode == 'xlsx') else open('{}.txt'.format(filename), 'w') as file_:

        if (config.formatcode == 'xlsx'):
            worksheet=file_.add_worksheet()

        cur=config.con.cursor()
        result=cur.execute('SELECT code FROM codes')
        codes=result.fetchall()

        for rows, row in enumerate(codes):
            if (config.formatcode == 'xlsx'):
                worksheet.write(rows, 0, row[0])
            else:
                file_.write('{}\n'.format(row[0]))

    clear()
    print(Fore.GREEN, '''
              ,     ,
             (\____/)
              (_oo_)
                (O)
              __||__    \)
           []/______\[] /
           / \______/ \/
          /    /__\
         (\   /____\   ''')
    print(
            Fore.YELLOW,
            '\n', 'El archivo {}.{} se ha exportado correctamente ;)'.format(filename, config.formatcode), '\n')
    sys.exit()

def main():
    banner()
    longoption()

if __name__ == '__main__':

    signals = [
            
                signal.SIGINT,
                signal.SIGTERM
                ]

    if (whoami != 'nt'):
        signals.extend([
            
            signal.SIGQUIT,
            signal.SIGUSR1,
            signal.SIGUSR2
            
        ])
    
    for _ in signals:
        signal.signal(_, protect)

    main()
