# Written by AnActualEmerald
# Last updated 5/20/21

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import write, remove
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from datetime import date, datetime
import time
import whathow

hostname = ""
serverPort = 8080


def load_bin(file):
    with open(file, "rb") as file:
        return file.read()


def clean_files(file_list):
    for file in file_list:
        remove(file)


class MemeServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        print(parsed_path.path)
        if parsed_path.path == "/whathow":
            q_parts = parse_qs(parsed_path.query)
            if not 'image' in q_parts.keys():
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(load_bin("./whathowlanding.html"))
                return
            req = Request(q_parts['image'][0], headers={'User-Agent': 'Mozilla/5.0'})
            img_path = f'./tmp/image_{datetime.now().microsecond}'
            with open(img_path, mode='xb') as image:
                with urlopen(req) as r:
                    image.write(r.read())
            video_path = whathow.gen_video(img_path)
            self.send_response(200)
            self.send_header("Content-type", "video/mp4")
            self.end_headers()
            self.wfile.write(
                load_bin(video_path))
            clean_files([img_path, video_path])
        else:
            print("dind't branch")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes("<html><head><title>Meme server Post Response</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(
                bytes("<p>This will send you memes at some point</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


    def do_POST(self):
        parsed_path = urlparse(self.path)
        print(parsed_path.path)
        if parsed_path.path == "/whathow":
            print("Branching to whathow")
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            img_path = f'./tmp/image_{datetime.now().microsecond}'
            with open(img_path, mode='xb') as image:
                image.write(post_body)
            video_path = whathow.gen_video(img_path)
            self.send_response(200)
            self.send_header("Content-type", "video/mp4")
            self.end_headers()
            self.wfile.write(
                load_bin(video_path))
            clean_files([img_path, video_path])
        else:
            print("dind't branch")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                bytes("<html><head><title>Meme server Post Response</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(
                bytes("<p>This will send you memes at some point</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

        # content_len = int(self.headers.get('Content-Length'))
        # post_body = self.rfile.read(content_len)

        # print(post_body)


if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverPort), MemeServer)
    print("Starting server at http://%s:%s" % (hostname, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Stopped server")
