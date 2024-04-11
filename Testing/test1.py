import asyncio
from bleak import BleakScanner
import socket
import json

MINDWAVE_NAME = "MindWave Mobile"

async def check_paired_and_connected():
    devices = await BleakScanner.discover()
    for device in devices:
        if MINDWAVE_NAME in device.name:
            print(f"Found paired device: {device.name} at {device.address}")
            return device.address
    return None

async def connect_to_tgc(address, host='127.0.0.1', port=13854):
    if address:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))
                print(f"Connected to ThinkGear Connector using {address}.")
                command = json.dumps({"enableRawOutput": True, "format": "Json"})
                sock.sendall(command.encode('utf-8'))

                data = sock.recv(1024)
                if data:
                    print("Data received from TGC:", data.decode())
                else:
                    print("No data received. Check the MindWave Mobile connection.")
        except Exception as e:
            print(f"Error connecting to ThinkGear Connector: {e}")
    else:
        print("MindWave Mobile device not found or not connected.")

async def main():
    paired_address = await check_paired_and_connected()
    await connect_to_tgc(paired_address)

if __name__ == "__main__":
    asyncio.run(main())
