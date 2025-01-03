import serial
import time
import csv

# Serial port configuration
SERIAL_PORT = "/dev/ttyUSB0"  # Change this to your serial port
BAUD_RATE = 9600  # Adjust as per your device
HEX_COMMAND = bytes.fromhex("01 03 00 00 00 01 85 DB")  # Replace with your HEX command

# File configuration
CSV_FILE = "serial_data.csv"

def initialize_csv(file_name):
    """Initialize the CSV file with headers."""
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Received Data"])
    print(f"Initialized {file_name}")

def append_to_csv(file_name, timestamp, data):
    """Append a row to the CSV file."""
    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, data])

def main():
    try:
        # Initialize the CSV file
        initialize_csv(CSV_FILE)

        # Open the serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")

        while True:
            # Send HEX command
            ser.write(HEX_COMMAND)
            print("Command sent:", HEX_COMMAND)

            # Wait for the response
            time.sleep(1)  # Adjust as per your device response time
            response = ser.read(ser.in_waiting)  # Read all available data

            if response:
                # Get timestamp and convert response to HEX
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                data_hex = response.hex()
                print(f"Received at {timestamp}: {data_hex}")

                # Save directly to CSV
                append_to_csv(CSV_FILE, timestamp, data_hex)

            # Uncomment the following line to break the loop after a specific condition
            # if some_condition:
            #     break

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    main()
