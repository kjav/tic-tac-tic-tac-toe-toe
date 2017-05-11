#!/usr/bin/env python 
from http.server import BaseHTTPRequestHandler, HTTPServer

import board

from board import create_board

import urllib

import os

import json

ref = None

main_board = None

# HTTPRequestHandler class
class TTTRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    global main_board
    if True:
      print(self.path)
      if self.path == "/":
        # Send response status code
        self.send_response(200)

        print(type(self.path))

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = str(main_board)
        print(message)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
      elif not (type(self.path) is None) and self.path.startswith("/create_board"):
        print("creating board")
        args = self.path.split('?')[1].split('&')
        if args[0] and args[1]:
          self.send_response(200)
          main_board = create_board(int(args[0].split('=')[1]), int(args[1].split('=')[1]))
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes(main_board))
        else:
          self.send_response(503)
          return
      elif not (type(self.path) is None) and self.path.startswith("/perform_move"):
        print("creating board")
        args = self.path.split('?')[1].split('&')
        if args[0] and args[1]:
          self.send_response(200)
          main_board.perform_move(args[0].split('=')[1], [tuple(r) for r in json.loads(args[1].split('=')[1])])
          self.send_header("Content-type", "text/html")
          self.end_headers()
          self.wfile.write(bytes(main_board))
        else:
          self.send_response(503)
          return
 
def run():
  b = create_board(3, 2)
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  ADDRESS = '127.0.0.1'
  PORT = 8080
  server_address = (ADDRESS, PORT)
  httpd = HTTPServer(server_address, TTTRequestHandler)
  print('running server at http://localhost:8080 ...')
  httpd.serve_forever()
 
 
run()
