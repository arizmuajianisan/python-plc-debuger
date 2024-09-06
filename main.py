from plcDebugger import PLCWriter, PLCReader
import os
import sys
import time

def write_mode(plc_writer, start_address, end_address, data):
    for address in range(start_address, end_address + 1):
        if address - start_address < len(data):
            result = plc_writer.write_to_plc(address, [data[address - start_address]])
            print(result)
        else:
            print(f"No data provided for address {address}")

def read_mode(plc_reader, start_address, end_address):
    for address in range(start_address, end_address + 1):
        result = plc_reader.read_plc(address)
        print(f"Read result for address {address}: {result}")

if __name__ == "__main__":
    # Get parameters from environment variables
    mode = os.environ.get('MODE')
    start_address = os.environ.get('START_ADDRESS')
    end_address = os.environ.get('END_ADDRESS')
    data = os.environ.get('DATA')
    modbus_host = os.environ.get('MODBUS_HOST')
    modbus_port = os.environ.get('MODBUS_PORT')
    loop = os.environ.get('LOOP', 'false').lower() == 'true'
    loop_delay = float(os.environ.get('LOOP_DELAY', '1'))  # Default to 1 second if not specified

    # Validate required environment variables
    if not all([mode, start_address, end_address, modbus_host, modbus_port]):
        print("Error: MODE, START_ADDRESS, END_ADDRESS, MODBUS_HOST, and MODBUS_PORT environment variables must be set")
        sys.exit(1)

    # Convert to appropriate types
    try:
        start_address = int(start_address)
        end_address = int(end_address)
        modbus_port = int(modbus_port)
        data = [int(x.strip()) for x in data.split(',')] if data else []
    except ValueError:
        print("Error: START_ADDRESS, END_ADDRESS, and MODBUS_PORT must be integers, and DATA must be comma-separated integers")
        sys.exit(1)

    plc_writer = PLCWriter(host=modbus_host, port=modbus_port)
    plc_reader = PLCReader(host=modbus_host, port=modbus_port)

    def perform_operation():
        if mode.lower() == 'w':
            write_mode(plc_writer, start_address, end_address, data)
        elif mode.lower() == 'r':
            read_mode(plc_reader, start_address, end_address)
        else:
            print(f"Invalid mode: {mode}")
            sys.exit(1)

    if loop:
        print(f"Running in loop mode with {loop_delay} second delay")
        while True:
            perform_operation()
            time.sleep(loop_delay)
    else:
        perform_operation()
