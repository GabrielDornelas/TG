#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import serial
comport = serial.Serial('COM1', 9600) 
print ('Serial Iniciada...\n')

import mysql.connector
cnx = mysql.connector.connect(user='root', password='root', host='127.0.0.1', port='9600')
cursor = cnx.cursor()
add_sinais = ("INSERT INTO sinais (sin_temp,sin_umid) VALUES (%s, %s)")

while (True):
  serialValue = comport.readline()
  data_sinais = serialValue.split("|")
  print (data_sinais)
  cursor.execute(add_sinais, data_sinais)
  cnx.commit()

cursor.close()
cnx.close()
comport.close()
