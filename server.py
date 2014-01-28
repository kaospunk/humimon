#!/usr/bin/env python

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
		self.wfile.write('{"temp":"' + values[1] + '","humidity":"' + values[2] + '","date":"' + date + '"}')
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
