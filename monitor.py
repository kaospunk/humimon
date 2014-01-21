#!/usr/bin/env python

import re                
import smtplib
import subprocess
import time
import datetime
import os
import signal

# Path to location of binary from the Adafruit repository
DHT_BIN = "Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver/Adafruit_DHT"

# Sensor type - 11, 22 or 2302
SENSOR = "2302"

# Data pin
PIN = "4"

DATA_FILE = "humidor_data"
EMAIL_ADDRESS = ""
DEBUG = True

def alert(temp,humidity):
	import smtplib

	fromaddr = EMAIL_ADDRESS 
	toaddrs = [EMAIL_ADDRESS]

	message = "From: {0}\n".format(fromaddr) 
	message += "To: {0}\n".format(fromaddr)
	message += "Subject: Humidor alert\n\n"
	message += "Current readings:\nTemperature: " + str(temp) + "\nHumidity: " + str(humidity)
	
	try:
		server = smtplib.SMTP('127.0.0.1')
		server.sendmail(fromaddr, toaddrs, message)
		server.quit()
	except:
		print_debug("Unable to send email")

def print_debug(message):
	if DEBUG:
		print message

temp_count = 0
humidity_count = 0	
while(True):
	ada_proc = subprocess.Popen([DHT_BIN, SENSOR, PIN],stdout=subprocess.PIPE);
	start = datetime.datetime.now()
	while ada_proc.poll() is None:
      		time.sleep(0.1)
      		now = datetime.datetime.now()
      		if (now - start).seconds> 10:
			try:
				print_debug("Trying to kill pid {0}".format(ada_proc.pid))
        			os.kill(ada_proc.pid, signal.SIGKILL)
        			os.waitpid(ada_proc.pid, os.WNOHANG)
			except:
				print_debug("Unable to kill process")
			continue
	output, err = ada_proc.communicate()
	matches = re.search("Temp =\s+([0-9.]+)", output)
	if (not matches):
		time.sleep(3)
		continue
        temp = float(matches.group(1))
	temp = (temp * 9/5) + 32

        # search for humidity printout
        matches = re.search("Hum =\s+([0-9.]+)", output)
        if (not matches):
		time.sleep(3)
		continue
        humidity = float(matches.group(1))

	out = open(DATA_FILE,"a")
	print_debug("{0:.1f}F  {1:.1f}%".format(temp,humidity))
	out.write("{0},{1:.1f},{2:.1f}\n".format(time.time(),temp,humidity))
	out.close()

	if temp < 65 or temp > 76:
		temp_count += 1
		if temp_count > 4:
			alert(temp,humidity)
			print_debug("temp out of range")
	else:
		temp_count = 0

	if humidity < 60 or humidity > 70:
		humidity_count += 1
		if humidity_count > 4:
			alert(temp,humidity)	
			print_debug("humidity out of range")
	else:
		humidity_count = 0

	time.sleep(3)
