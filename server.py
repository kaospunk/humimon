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


# This relies on AdvancedHTTPServer from https://gist.github.com/zeroSteiner/4502576

from AdvancedHTTPServer import *
import logging
import os
import re
import shutil
import subprocess
import time

WEB_ROOT = "humi/"
DATA_FILE = "humidor_data"

class MyHandler(AdvancedHTTPServerRequestHandler):
        def install_handlers(self):
                self.handler_map[''] = self.Incoming

        def Incoming(self, query):
		if self.path == 'humi.css':
			self.respond_file(WEB_ROOT + 'humi.css')
			return
		if self.path == 'hygro.jpg':
			self.respond_file(WEB_ROOT + 'hygro.jpg')
			return
		if self.path == 'DS-DIGII.TTF':
			self.respond_file(WEB_ROOT + 'DS-DIGII.TTF')
			return
		self.send_response(200)
		self.end_headers()
		a = open(DATA_FILE,'r')
		lines = a.read().split('\n')
		values = lines[-2].split(',')
		date = time.strftime('%m/%d/%Y %H:%M:%S',time.localtime(float(values[0])))
		self.wfile.write('<html><head><meta http-equiv="refresh" content="3"><link href="humi.css" rel="stylesheet" type="text/css"></head><body>')
		self.wfile.write('<div id="container"><img id="image" src="hygro.jpg"/>')
  		self.wfile.write('<p id="temp">{0}</p>\n'.format(values[1]))
  		self.wfile.write('<p id="humidity">{0}<p>\n'.format(values[2]))
		self.wfile.write('<p id="date">{0}</p>\n'.format(date))
		self.wfile.write('</div></body></html>')
		a.close()

def main():
        server = AdvancedHTTPServer(MyHandler,address=('0.0.0.0',8080))
        server.server_version = 'Humimon'

        main_file_handler = logging.handlers.RotatingFileHandler("humiweb.log", maxBytes = 262144, backupCount = 1)
        main_file_handler.setLevel(logging.DEBUG)
        main_file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)-30s %(levelname)-10s %(message)s"))
        logging.getLogger('').setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(main_file_handler)

        server.serve_forever(True)

if __name__ == '__main__':
	main()
