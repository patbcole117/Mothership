from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import http.client
import time

DEFAULT_MOTHERSHIP_ADDRESS = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8000

LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 8001

DEFAULT_DURATION = 5

def main():
    local_channel_thread = open_local_channel(LOCAL_ADDRESS, LOCAL_PORT)
    while True:
        mission_plan = phone_home(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)
        print(mission_plan)
        if local_channel_thread.is_alive():
            print('LOCAL CHANNEL IS OPEN')
        else:
            local_channel_thread = open_local_channel(LOCAL_ADDRESS, LOCAL_PORT)
        time.sleep(DEFAULT_DURATION)
        

def phone_home(mothership_ip: str, mothership_port: int):

    print('PHONE HOME...')

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    try:
        conn.request("GET", "/")
        r = conn.getresponse()
        return r.read().decode()
    except ConnectionRefusedError as err:
        print(err)
        print('CONNECTION TO MOTHERSHIP REFUSED.')


def open_local_channel(local_ip: str, local_port: int, duration: int = 5):
    
    print(f'CREATING NEW LOCAL CHANNEL THREAD...')

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