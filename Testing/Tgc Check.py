import socket
import json

def check_tgc_connection():
    host = '127.0.0.1'  # ThinkGear Connector host
    port = 13854        # ThinkGear Connector port

    # Create a socket connection to ThinkGear Connector
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            print("Connected to ThinkGear Connector.")

            # Send a command to TGC to get the status. Adjust the command as per TGC's API
            command = json.dumps({"enableRawOutput": True, "format": "Json"})
            sock.sendall(command.encode('utf-8'))

            # Wait and read the response
            response = sock.recv(1024).decode('utf-8')
            if response:
                print("Received data from ThinkGear Connector.",response)
                return True
            else:
                print("No data received from ThinkGear Connector.")
                return False
        except socket.error as e:
            print(f"Cannot connect to ThinkGear Connector: {e}")
            return False

if __name__ == "__main__":
    if check_tgc_connection():
        print("ThinkGear Connector is operational and connected to Mindwave Mobile 2.")
    else:
        print("ThinkGear Connector may not be operational or not connected to Mindwave Mobile 2.")
