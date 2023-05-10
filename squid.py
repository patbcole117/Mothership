import http.client

DEFAULT_MOTHERSHIP_IP = "127.0.0.1"
DEFAULT_MOTHERSHIP_PORT = 8001


def main():
    mission_plan = phone_home(DEFAULT_MOTHERSHIP_IP, DEFAULT_MOTHERSHIP_PORT)
    print(mission_plan)

def phone_home(mothership_ip: str, mothership_port: int):
    conn = http.client.HTTPConnection(mothership_ip, mothership_port)
    conn.request("GET", "/")
    r = conn.getresponse()
    return r.read().decode()


if __name__ == "__main__":
    main()