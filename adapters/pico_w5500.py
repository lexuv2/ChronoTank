import adapters.base_adapter
import subprocess
import serial
import time



class pico_w5500(adapters.base_adapter.Adapter):
    def __init__(self, serial_port="/dev/ttyACM0", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.ser = serial.Serial(serial_port, baudrate, timeout=1)
        self.ser.write(('\n\r').encode())
        while True:
            line = self.ser.readline().decode(errors='ignore')
            if line.strip()== '':
                break
            print(line.strip())
        

        print(f"Connected to {self.serial_port} at {self.baudrate} baud.")



    def run(self, inp):

        print(f"Sending input: {(inp.decode() + '\n\r').encode()}")
        self.ser.write((inp.decode() + '\n\r').encode())
        
        # ser.flush()
        # Read response(s)
        time.sleep(0.1)
        while True:
            line = self.ser.readline().decode(errors='ignore')
            print(line.strip())
            try:
                return int(line.strip())
            except ValueError:
                continue
        return -1
