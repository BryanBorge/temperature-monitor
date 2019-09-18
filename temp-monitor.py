from time import sleep
import Adafruit_DHT
import schedule
from Adafruit_CharLCD import Adafruit_CharLCD
import collections
import dweepy
import requests

lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)

def readDHT11(sensor, pin):
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	while humidity is None or temperature is None:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	temperature = temperature * 9.0/5.0 + 32
	return(humidity, temperature)

def senddweet(temp,humidity):
	dweepy.dweet_for('TempMonitor', {'Temp':int(temp), 'Humid' : int(humidity)})

def Monitor():
	sensor = 11
	pin = 4
	temp = 0
	humidity = 0
	minHumidity = 0
	maxHumidity = 0
	minTemp = 0
	maxTemp = 0
	readingCount = 1
	schedule.every(30).seconds.do(lambda: senddweet(temp,humidity))
	try:
		while True:
			humidity, temp = readDHT11(sensor, pin)

			if readingCount == 1:
				minHumidity = maxHumidity = humidity
				minTemp = maxTemp = temp
			else: 
				minTemp = temp if temp < minTemp else minTemp 
				maxTemp = temp if temp > maxTemp else maxTemp
				minHumidity = humidity if humidity < minHumidity else minHumidity
				maxHumidity = humidity if humidity > maxHumidity else maxHumidity
			try:
				schedule.run_pending()
			except requests.exceptions.SSLError as e:
				print('Dweet error\n')

			lcd.clear()		
			lcd.message('Humidity: {0} \n'.format(int(humidity)))
			lcd.message('Min: {0} Max: {1}'.format(int(minHumidity), int(maxHumidity)))
			sleep(3)
			lcd.clear()
			lcd.message('Temperature: {0} \n'.format(int(temp)))
			lcd.message('Min: {0} Max: {1}'.format(int(minTemp), int(maxTemp)))
			sleep(2)

			readingCount = readingCount + 1
	except KeyboardInterrupt:
		lcd.clear()
		
if __name__ == '__main__':
	Monitor()
