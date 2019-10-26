import time
import os
import datetime
import Adafruit_DHT
import schedule
from Adafruit_CharLCD import Adafruit_CharLCD
import collections
import dweepy
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

def InitSheet():
	scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json',scope)
	client = gspread.authorize(creds)
	sheet = client.open('TentMonitor').sheet1
	return sheet
	
def readDHT11(sensor, pin):
	humidity = None
	temperature = None

	while humidity is None or temperature is None:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	temperature = temperature * 9.0/5.0 + 32
	return(humidity, temperature)

def senddweet(temp,humidity):
	dweepy.dweet_for('TempMonitor', {'Temp':int(temp), 'Humid' : int(humidity)})

def savedata(temp, humid):
	sheet = InitSheet()	
	insert_row = [str(datetime.datetime.now()),temp, humid]
	insert_index = len(sheet.get_all_records())
	sheet.insert_row(insert_row,insert_index+2)
	print('saved')

def runpending(schedule):
	try:
		schedule.run_pending()
	except requests.exceptions.SSLError as e:
		print('SSL Error\n')
		print(e)
	except requests.exceptions.ConnectionError as er:
		print('HTTPConnectionPool Error\n')
		print(er)

def printLCD(h, t):
	lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)	
	lcd.clear()		
	lcd.message('Humidity: {0} \n'.format(int(h)))
	lcd.message('Temperature: {0} \n'.format(int(t)))	

def Monitor():
	sensor = 11
	pin = 4
	temp = 0
	humidity = 0
	readingCount = 1
	schedule.every(30).seconds.do(lambda: senddweet(temp,humidity))
	schedule.every(10).minutes.do(lambda: savedata(temp,humidity))
		
	try:
		while True:
			humidity, temp = readDHT11(sensor, pin)
			print('{0} \nHumidity: {1} %'.format(readingCount, int(humidity)))
			print('Temperature: {0} F\n'.format(int(temp)))
			printLCD(humidity, temp)
			runpending(schedule)
			readingCount += 1

	except KeyboardInterrupt:
		lcd.clear()
		print('Goodbye')

if __name__ == '__main__':
	Monitor()
