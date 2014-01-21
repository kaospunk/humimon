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

from AdvancedHTTPServer import *
import logging
import subprocess
import time

WEB_ROOT = "humi/"
DATA_FILE = "humidor_data"

class MyHandler(AdvancedHTTPServerRequestHandler):
        def install_handlers(self):
                self.handler_map['get_data'] = self.Incoming

        def Incoming(self, query):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		a = open(DATA_FILE,'r')
		lines = a.read().split('\n')
		values = lines[-2].split(',')
		date = time.strftime('%m/%d/%Y %H:%M:%S',time.localtime(float(values[0])))
		self.wfile.write('{"temp":' + values[1] + ',"humidity":' + values[2] + ',"date":"' + date + '"}')
		a.close()

def main():
        server = AdvancedHTTPServer(MyHandler,address=('0.0.0.0',8080))
        server.server_version = 'Humimon'
	server.serve_files = True
	server.serve_files_root = WEB_ROOT

        main_file_handler = logging.handlers.RotatingFileHandler("humiweb.log", maxBytes = 262144, backupCount = 1)
        main_file_handler.setLevel(logging.DEBUG)
        main_file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)-30s %(levelname)-10s %(message)s"))
        logging.getLogger('').setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(main_file_handler)

        server.serve_forever(True)

if __name__ == '__main__':
	main()
