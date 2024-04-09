import subprocess
import asyncio
from pylsl import StreamInlet, resolve_stream
from collections.abc import MutableMapping

# Function to start the mindwavelsl tool
def start_mindwavelsl():
    # Command to run mindwavelsl
    cmd = ['mindwavelsl', '--host', 'localhost', '--port', '13854']
    return subprocess.Popen(cmd)

# Function to fetch and print EEG data from LSL
async def fetch_eeg_data():
    print("Looking for an EEG stream...")
    while True:
        streams = resolve_stream('type', 'EEG')
        if streams:
            inlet = StreamInlet(streams[0])
            print("Connected to EEG stream.")
            while True:
                sample, timestamp = inlet.pull_sample()
                print(f"Timestamp: {timestamp}, EEG sample: {sample}")
        else:
            print("No EEG stream found. Retrying...")
            await asyncio.sleep(5)  # Wait a bit before retrying

async def main():
    # Start the mindwavelsl tool
    mindwave_process = start_mindwavelsl()
    
    try:
        # Fetch EEG data
        await fetch_eeg_data()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping...")
    finally:
        # Ensure the subprocess is terminated
        mindwave_process.terminate()

if __name__ == '__main__':
    asyncio.run(main())
