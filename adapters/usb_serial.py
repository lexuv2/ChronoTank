import adapters.base_adapter
import subprocess
import serial
import time

class USBSerial(adapters.base_adapter.Adapter):
    def __init__(self, serial_port="/dev/ttyACM0", baudrate=115200):
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.ser = serial.Serial(serial_port, baudrate, timeout=1)



    def run(self, inp):


        time_start = time.perf_counter_ns() 
        self.ser.write((inp.decode() + '\r\n').encode())
        
        # ser.flush()
        # Read response(s)
        while True:
            line = self.ser.readline().decode(errors='ignore')
            if not line:
                break
            # print(line)
            if 'OK' in line or 'FAIL' in line:
                return time.perf_counter_ns() - time_start
        return -1
