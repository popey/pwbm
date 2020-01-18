#!/usr/bin/python3

import http.server
import socketserver
import os

web_dir = os.path.join(os.getenv('SNAP_USER_COMMON'), 'archive')
os.chdir(web_dir)
PORT = 8076

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()