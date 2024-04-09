import socket
import json
import time

def check_tgc_connection(timeout=5):
    host = '127.0.0.1'  # ThinkGear Connector host
    port = 13854        # ThinkGear Connector port
    buffer_size = 2048  # Define the buffer size for receiving data

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            sock.settimeout(timeout)  # Set a timeout for the socket
            print("Connected to ThinkGear Connector.")

            # Send a command to TGC to request data
            command = json.dumps({"enableRawOutput": True, "format": "Json"})
            sock.sendall(command.encode('utf-8'))

            end_time = time.time() + timeout
            while time.time() < end_time:
                try:
                    response = sock.recv(buffer_size).decode('utf-8')
                    if response:
                        data = json.loads(response)
                        print(f"Received data: {data}")
                        if 'poorSignalLevel' in data:
                            print(f"Signal Level: {data['poorSignalLevel']}")
                            if data['poorSignalLevel'] < 50:  # Adjust based on your signal quality criteria
                                print("Good signal from Mindwave Mobile 2.")
                                return True
                    else:
                        print("No data received. Checking again...")
                except socket.timeout:
                    print("Socket timed out. No data received.")
                    break  # Exit the loop if no data is received within the timeout period
                except json.JSONDecodeError:
                    # Handle incomplete JSON parsing
                    print("Received incomplete data. Continuing...")

            print("Checking completed. Mindwave Mobile 2 may not be properly connected.")
            return False
        except socket.error as e:
            print(f"Cannot connect to ThinkGear Connector: {e}")
            return False

if __name__ == "__main__":
    if check_tgc_connection():
        print("ThinkGear Connector is operational and connected to Mindwave Mobile 2.")
    else:
        print("ThinkGear Connector may not be operational or not connected to Mindwave Mobile 2.")
