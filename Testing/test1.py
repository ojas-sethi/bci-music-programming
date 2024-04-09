import asyncio
from bleak import BleakClient, BleakScanner


async def scan_and_return_address():
    device_name = "MindWave Mobile"
    devices = await BleakScanner.discover()

    for device in devices:
        print(f"Found device: {device.name}")
        if device.name == device_name:
            print(f"Found {device_name} at address {device.address}")
            return device.address
                # Add your code here to interact with the Mindwave Mobile 2
    else:
        print(f"{device_name} not found")
        return None
    
MINDWAVE_ADDRESS = None 

async def connect_and_listen(address):
    CHARACTERISTIC_UUID =  None
    async with BleakClient(address) as client:
        if await client.is_connected():
            print("Connected to the Mindwave Mobile 2")
            services = await client.get_services()

            for service in services:
                for char in service.characteristics:
                    print(f"  Characteristic {char} -> {char.uuid}")
                    if "EEG" in char.description:
                        print(f"This might be the EEG raw data characteristic (UUID: {char.uuid})")
                        CHARACTERISTIC_UUID = char.uuid
                 
            if CHARACTERISTIC_UUID is None:
                print("No EEG characteristic found")
                return
            else:
            
                def callback(sender, data):
                    # Parse the incoming data
                    # Mindwave Mobile 2 uses a specific format that you will need to decode
                    print(f"Raw data: {data}")

                await client.start_notify(CHARACTERISTIC_UUID, callback)

                # Keep the script running to continue receiving data
                await asyncio.sleep(300)  # Run for 5 minutes, adjust as necessary
        else:
            print("Failed to connect")


if __name__ == "__main__":
    if MINDWAVE_ADDRESS == None:
        MINDWAVE_ADDRESS = asyncio.run(scan_and_return_address())

    if MINDWAVE_ADDRESS:
        continue_reading = True
        asyncio.run(connect_and_listen(MINDWAVE_ADDRESS))
