#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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

def alert(temp,humidity):
	import smtplib

	fromaddr = EMAIL_ADDRESS 
	toaddrs = [EMAIL_ADDRESS]

	message = "From: {0}\n".format(fromaddr) 
	message += "To: {0}\n".format(fromaddr)
	message += "Subject: Humidor alert\n\n"
	message += "Current readings:\nTemperature: " + str(temp) + "\nHumidity: " + str(humidity)

	server = smtplib.SMTP('127.0.0.1')
	server.sendmail(fromaddr, toaddrs, message)
	server.quit()
	
while(True):
	ada_proc = subprocess.Popen([DHT_BIN, SENSOR, PIN],stdout=subprocess.PIPE);
	start = datetime.datetime.now()
	while ada_proc.poll() is None:
      		time.sleep(0.1)
      		now = datetime.datetime.now()
      		if (now - start).seconds> 10:
        		os.kill(ada_proc.pid, signal.SIGKILL)
        		os.waitpid(-1, os.WNOHANG)
			continue
	output, err = ada_proc.communicate()
	matches = re.search("Temp =\s+([0-9.]+)", output)
	if (not matches):
		print "no match"
		time.sleep(3)
		continue
        temp = float(matches.group(1))
	temp = (temp * 9/5) + 32

        # search for humidity printout
        matches = re.search("Hum =\s+([0-9.]+)", output)
        if (not matches):
		print "no match"
		time.sleep(3)
		continue
        humidity = float(matches.group(1))

	out = open(DATA_FILE,"a")
	print temp
	print humidity
	print time.time()
	out.write("{0},{1:.1f},{2:.1f}\n".format(time.time(),temp,humidity))
	out.close()

	if temp < 65 or temp > 76:
		alert(temp,humidity)
		print "temp out of range"
	if humidity < 60 or humidity > 70:
		print "humidity out of range"
		alert(temp,humidity)	
	time.sleep(3)
