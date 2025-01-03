import serial
import time
from openpyxl import Workbook

# Serial port configuration
SERIAL_PORT = "/dev/ttyUSB0"  # Change this to your serial port
BAUD_RATE = 9600  # Adjust as per your device
HEX_COMMAND = bytes.fromhex("01 03 00 00 00 01 85 DB")  # Replace with your HEX command

# Excel file configuration
EXCEL_FILE = "serial_data.xlsx"

def save_to_excel(data_list):
    # Create a new workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Serial Data"

    # Add headers
    ws.append(["Timestamp", "Received Data"])

    # Add data rows
    for timestamp, data in data_list:
        ws.append([timestamp, data])

    # Save the Excel file
    wb.save(EXCEL_FILE)
    print(f"Data saved to {EXCEL_FILE}")

def main():
    try:
        # Open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        # Prepare to store data
        received_data = []

        while True:
            # Send HEX command
            ser.write(HEX_COMMAND)
            print("Command sent:", HEX_COMMAND)

            # Wait for the response
            time.sleep(1)  # Adjust as per your device response time
            response = ser.read(ser.in_waiting)  # Read all available data

            if response:
                # Decode and store the response
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                data_hex = response.hex()
                print(f"Received at {timestamp}: {data_hex}")
                received_data.append((timestamp, data_hex))

            # Stop after collecting some data (optional)
            if len(received_data) >= 10:  # Adjust this limit as needed
                break

        # Save the collected data to an Excel file
        save_to_excel(received_data)

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
