from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import http.client
import time
import uuid
import socket

DEFAULT_MOTHERSHIP_ADDRESS = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8000

LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 8001
LOCAL_COMMS = False

DEFAULT_DURATION = 5

def main():

    r = register(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)

    if LOCAL_COMMS:
        local_comms_thread = open_local_comms(LOCAL_ADDRESS, LOCAL_PORT)

    while True:
        orders = phone_home(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)
        print(orders)

        if LOCAL_COMMS and not (local_comms_thread.is_alive()):
                local_comms_thread = open_local_comms(LOCAL_ADDRESS, LOCAL_PORT)

        time.sleep(DEFAULT_DURATION)
    
        

def register(mothership_ip, mothership_port):

    mac = uuid.getnode()
    hostname = socket.gethostname()
    date_created = time.time() 

    params = f'{{"id": "{hostname}-{mac}","name": "{hostname}-{mac}", "hostname": "{hostname}", "mac": "{mac}", "date_created": "{date_created}"}}'.encode()
    print(params)
    content_length = len(params)
    content_type = 'application/json'
    headers = {"Content-Type": content_type, "Content-Length": content_length}

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    try:
        conn.request("POST", "/register/", params, headers)
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        print(err)
        print('CONNECTION TO MOTHERSHIP REFUSED.')


def phone_home(mothership_ip, mothership_port):

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    try:
        conn.request("GET", "/home")
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        print(err)
        print('CONNECTION TO MOTHERSHIP REFUSED.')


def open_local_comms(local_ip, local_port):

    local_channel_server = ThreadingHTTPServer((LOCAL_ADDRESS, LOCAL_PORT), LocalHandler)
    local_channel_thread = threading.Thread(target=local_channel_server.serve_forever)
    local_channel_thread.daemon = True
    local_channel_thread.start()
    
    return local_channel_thread


class LocalHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        message = threading.current_thread().name
        self.wfile.write(message.encode())
        self.wfile.write('\n'.encode())
        return

    def do_POST(self):
        
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length)
        print(body.decode())

        self._set_headers()
        return


if __name__ == "__main__":
    main()