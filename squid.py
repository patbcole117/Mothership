from  http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import http.client
import time

DEFAULT_MOTHERSHIP_ADDRESS = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8000

LOCAL_ADDRESS = "127.0.0.1"
LOCAL_PORT = 8001


def main():
    for i in range(5):
        print(f'ITERATION: {i}\n')
        mission_plan = phone_home(DEFAULT_MOTHERSHIP_ADDRESS, DEFAULT_MOTHERSHIP_PORT)
        print(mission_plan)
        open_local_channel(LOCAL_ADDRESS, LOCAL_PORT)
        

def phone_home(mothership_ip: str, mothership_port: int):

    print('PHONE HOME...')

    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    conn.request("GET", "/")
    r = conn.getresponse()
    return r.read().decode()

def open_local_channel(local_ip: str, local_port: int, duration: int = 5):
    
    print(f'OPENING LOCAL CHANNEL FOR {duration} SECONDS...')

    timeout = time.time() + duration
    server = ThreadingHTTPServer((LOCAL_ADDRESS, LOCAL_PORT), LocalHandler)
    while time.time() < timeout:
        server.handle_request()

    print(f'CLOSING LOCAL CHANNEL...')


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