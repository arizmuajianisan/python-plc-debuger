from pyModbusTCP.client import ModbusClient
from datetime import datetime
import time
import sys
import logging
import os


class PLCWriter:
    """
    Initialize PLCWriter
    Get the host and port from the environment variables
    """

    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Try to get modbus host and port from environment variable
        try:
            self.host = os.getenv("MODBUS_HOST")
            self.port = int(os.getenv("MODBUS_PORT"))
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve host and port from environment variables. {e}"
            )
            sys.exit(1)

        # Initialize connection to PLC
        self.plc = ModbusClient(
            host=self.host,
            port=self.port,
            auto_open=True,
        )

    def write_to_plc(self, address, data):
        """
        Write data to PLC
        :param address: address to write to
        :param data: data to write
        :return: execution time
        """
        result = self.plc.write_multiple_registers(address, data)
        if result:
            self.logger.info(f"Wrote data to PLC at address {address}: {data}")
            return result
        else:
            error_message = f"Failed to write data to PLC at address {address}."
            self.logger.error(error_message)
            return error_message


class PLCReader:
    """
    Class to read data from PLC
    Get the host and port from the environment variables
    """

    def __init__(self):
        # Set up logging
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Try to get modbus host and port from environment variables
        try:
            self.host = os.getenv("MODBUS_HOST")
            self.port = int(os.getenv("MODBUS_PORT"))
        except Exception as e:
            self.logger.error(
                f"Failed to retrieve host and port from environment variables. {e}"
            )
            sys.exit(1)

        # Initialize connection to PLC
        self.plc = ModbusClient(
            host=self.host,
            port=self.port,
            auto_open=True,
        )

    def read_plc(self, start_address, num_registers=1):
        """
        Read data from PLC
        :param start_address: start address to read from
        :param num_registers: number of registers to read (default: 1)
        :return: data read from PLC
        """
        try:
            result = self.plc.read_holding_registers(start_address, num_registers)
            if result:
                if num_registers == 1:
                    self.logger.info(
                        f"Read value at address {start_address}: {result[0]}"
                    )
                    return result[0]
                else:
                    self.logger.info(
                        f"Read {num_registers} values starting from address {start_address}: {result}"
                    )
                    return result
            else:
                self.logger.error(
                    f"Failed to read {num_registers} register(s) from address {start_address}"
                )
                return None
        except Exception as e:
            self.logger.error(f"Error reading from PLC: {e}")
            return None


# Example usage
if __name__ == "__main__":
    plc_writer = PLCWriter()

    while True:
        plc_writer.write_time_to_plc(100)
        time.sleep(0.2)

    plc_reader = PLCReader()

    # Read single register
    plc_reader.read_plc(100)

    # Read multiple registers
    plc_reader.read_plc(100, 6)  # Read 6 registers starting from address 100
