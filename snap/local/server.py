#!/usr/bin/python3

import http.server
import socketserver
import os

base_folder = os.getenv('SNAP_USER_COMMON') if os.getenv("SNAP") else \
    os.path.join(os.path.dirname(__file__), "..", "..")
web_dir = os.path.join(base_folder, 'archive')
os.chdir(web_dir)
PORT = 8076

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()