from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8001


class GetHandler(BaseHTTPRequestHandler):
    # TODO
    
server = ThreadingHTTPServer(((SERVER_ADDRESS, SERVER_PORT), GetHandler))
server.serve_forever()