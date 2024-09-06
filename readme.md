# PLC Debugger

This is part of an internal project to create an IoT network communication between a PLC and a computer server. The communication protocol is based on the Modbus protocol.

## Requirements

- Python 3.9+
- Docker (recommended for running the program in a containerized environment)

## How to use

### Using Python

1. Clone the repository
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the program:
   ```bash
   python main.py
   ```

### Using Docker

1. Clone the repository
2. Build the Docker image:
   ```bash
   docker build -t plc-debugger .
   ```
3. Run the Docker container:

   Examples of usage:

   a. Read operation (single execution):
   ```bash
   docker run --name plc-read -e MODE=r -e START_ADDRESS=100 -e END_ADDRESS=105 -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 plc-debugger
   ```

   b. Write operation (single execution):
   ```bash
   docker run --name plc-write -e MODE=w -e START_ADDRESS=100 -e END_ADDRESS=105 -e DATA="1,2,3,4,5,6" -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 plc-debugger
   ```

   c. Read operation in loop mode:
   ```bash
   docker run --name plc-read-loop -e MODE=r -e START_ADDRESS=100 -e END_ADDRESS=105 -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 -e LOOP=true -e LOOP_DELAY=5 plc-debugger
   ```

   d. Write operation in loop mode:
   ```bash
   docker run --name plc-write-loop -e MODE=w -e START_ADDRESS=100 -e END_ADDRESS=105 -e DATA="1,2,3,4,5,6" -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 -e LOOP=true -e LOOP_DELAY=10 plc-debugger
   ```

   e. Read operation with custom register type and data type:
   ```bash
   docker run --name plc-read-custom -e MODE=r -e START_ADDRESS=100 -e END_ADDRESS=105 -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 -e REGISTER_TYPE=input -e DATA_TYPE=float plc-debugger
   ```

   f. Write operation with custom byte and word order:
   ```bash
   docker run --name plc-write-custom -e MODE=w -e START_ADDRESS=100 -e END_ADDRESS=105 -e DATA="1.5,2.7,3.14" -e MODBUS_HOST=192.168.1.100 -e MODBUS_PORT=502 -e DATA_TYPE=float -e BYTE_ORDER=little -e WORD_ORDER=little plc-debugger
   ```

   Environment variables:
   - `MODE`: 'r' for read, 'w' for write
   - `START_ADDRESS`: starting address to read/write
   - `END_ADDRESS`: ending address to read/write
   - `MODBUS_HOST`: IP address of the PLC
   - `MODBUS_PORT`: Modbus port of the PLC (usually 502)
   - `DATA`: comma-separated values to write (required for write mode)
   - `LOOP`: set to 'true' to enable loop mode
   - `LOOP_DELAY`: delay in seconds between iterations in loop mode (default: 1)
   - `REGISTER_TYPE`: 'holding' (default) or 'input' for reading different register types
   - `DATA_TYPE`: 'int' (default) or 'float' for specifying the data type
   - `BYTE_ORDER`: 'big' (default) or 'little' for specifying the byte order
   - `WORD_ORDER`: 'big' (default) or 'little' for specifying the word order when using float data type

   Note on container lifecycle:
   - In single execution mode (default), the container will run once and then exit.
   - In loop mode (LOOP=true), the container will continue running indefinitely until stopped manually.

   To stop a running container in loop mode, use:
   ```bash
   docker stop <container_name>
   ```
   For example:
   ```bash
   docker stop plc-read-loop
   ```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.


