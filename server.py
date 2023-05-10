from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8001


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.current_thread().name
        self.wfile.write('This is a test.\n'.encode())
        self.wfile.write('This is another test.'.encode())
        return


server = ThreadingHTTPServer((SERVER_ADDRESS, SERVER_PORT), GetHandler)
server.serve_forever()