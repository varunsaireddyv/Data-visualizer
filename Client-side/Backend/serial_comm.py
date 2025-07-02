
import serial
import time

class SerialComm:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"[✓] Connected to {self.port} @ {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"[!] Failed to connect: {e}")

    def send(self, msg: str):
        if self.ser:
            self.ser.write((msg + '\n').encode())

    def receive(self):
        if self.ser and self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return None

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[x] Serial connection closed.")

if __name__ == "__main__":
    comm = SerialComm()
    comm.connect()
    comm.send("get all")
    time.sleep(0.5)
    print(comm.receive())
    comm.disconnect()
