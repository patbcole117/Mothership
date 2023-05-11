from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import http.client
import time

DEFAULT_MOTHERSHIP_ADDRESS = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8000

LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 8001
LOCAL_COMMS = False

DEFAULT_DURATION = 5

def main():

    register(LOCAL_ADDRESS, LOCAL_PORT)

    if LOCAL_COMMS:
        local_comms_thread = open_local_comms(LOCAL_ADDRESS, LOCAL_PORT)

    while True:
        orders = phone_home(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)
        print(orders)

        if LOCAL_COMMS and not (local_comms_thread.is_alive()):
                local_comms_thread = open_local_comms(LOCAL_ADDRESS, LOCAL_PORT)

        time.sleep(DEFAULT_DURATION)
    
        

def register(mothership_ip: str, mothership_port: int):

    params = '{"MAC": 123456, "HOSTNAME": "TEST", "MESSAGE": "HELLO"}'.encode()

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    try:
        conn.request("POST", "/register", params)
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        print(err)
        print('CONNECTION TO MOTHERSHIP REFUSED.')


def phone_home(mothership_ip: str, mothership_port: int):

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    try:
        conn.request("GET", "/home")
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        print(err)
        print('CONNECTION TO MOTHERSHIP REFUSED.')


def open_local_comms(local_ip: str, local_port: int):

    local_channel_server = ThreadingHTTPServer((LOCAL_ADDRESS, LOCAL_PORT), LocalHandler)
    local_channel_thread = threading.Thread(target=local_channel_server.serve_forever)
    local_channel_thread.daemon = True
    local_channel_thread.start()
    
    return local_channel_thread


class LocalHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        message = threading.current_thread().name
        self.wfile.write(message.encode())
        self.wfile.write('\n'.encode())
        return

if __name__ == "__main__":
    main()