#!/usr/bin/env python
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from python.board import create_board

all_boards = dict()

# HTTPRequestHandler class
class TTTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get path", self.path)
        if self.path is not None and self.path.startswith("/create_board"):
            print("creating board")
            args = self.path.split("?")[1].split("&")
            if len(args) == 3:
                self.send_response(301)
                board = create_board(
                    int(args[0].split("=")[1]), int(args[1].split("=")[1])
                )
                all_boards[int(args[2].split("=")[1])] = board
                self.send_header("Location", "play.html")
                self.end_headers()
                # self.wfile.write(b'play.html')
                return
            else:
                self.send_response(503)
                return
        elif self.path is not None and self.path.startswith("/print_board"):
            print("printing board")
            args = self.path.split("?")[1].split("&")
            if len(args) == 1:
                self.send_response(200)
                board = all_boards[int(args[0].split("=")[1])]
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(board))
                return
            else:
                self.send_response(503)
                return
        elif self.path is not None and self.path.startswith("/perform_move"):
            print("creating board")
            args = self.path.split("?")[1].split("&")
            if len(args) == 3:
                self.send_response(200)
                board = all_boards[args[2]]
                board.perform_move(
                    args[0].split("=")[1],
                    [tuple(r) for r in json.loads(args[1].split("=")[1])],
                )
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(board))
            else:
                self.send_response(503)
                return
        else:
            if self.path == "/":
                self.path = "/index.html"

            filename = os.path.join("../public", *self.path.split("/"))
            if not os.path.exists(filename):
                # Send response status code
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return

            mtype = mimetypes.guess_type(self.path)[0]
            if mtype is None:
                mtype = "text/html"
            # Send response status code
            self.send_response(200)
            # Send headers
            self.send_header("Content-type", mtype)
            self.end_headers()

            # Write content as utf-8 data
            with open(filename, "rb") as f:
                self.wfile.write(f.read())
            return


def run():
    b = create_board(3, 2)
    print("starting server...")

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server,
    # you need root access
    ADDRESS = "127.0.0.1"
    PORT = 8080
    server_address = (ADDRESS, PORT)
    httpd = HTTPServer(server_address, TTTRequestHandler)
    print("running server at http://localhost:8080 ...")
    httpd.serve_forever()


run()
