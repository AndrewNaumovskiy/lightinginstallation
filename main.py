import serial
import time
import sys
import threading

class DMX:
    def __init__(self,COM='/dev/ttyUSB0',Cnumber=512,Brate=250000,Bsize=8,StopB=2):
        #start serial
        self.com = COM
        self.channel_num = Cnumber + 1
        self.Brate = Brate
        self.Bsize = Bsize
        self.StopB = StopB
        self.data = [0] * self.channel_num
        self.data[0] = 0 # StartCode
        self.sleepms = 50.0
        self.breakus = 176.0
        self.MABus = 16.0

        self.send_thread = threading.Thread(target=self.loop)
        self.send_thread.daemon = True

    def start(self):
        try:
            self.ser = serial.Serial(self.com,baudrate=self.Brate,bytesize=self.Bsize,stopbits=self.StopB)
            self.startThread()
        except value:
            print("start error", value)

    def set_data(self,id,data):
        self.data[id]=data

    def set_array(self, pass_array):
        for i in range(len(pass_array)):
            self.data[i+1] = pass_array[i]

    def send(self):
        try:
            # Send Break : 88us - 1s
            self.ser.break_condition = True
            time.sleep(self.breakus/1000000.0)

            # Send MAB : 8us - 1s
            self.ser.break_condition = False
            time.sleep(self.MABus/1000000.0)

            # Send Data
            self.ser.write(bytearray(self.data))
            self.ser.write(bytearray(self.data))

            # Sleep
            time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

        except ValueError:
            print("oops", ValueError)

    def sendzero(self):
        self.data = [0] * self.channel_num
        self.send()

    def stop(self):
        self.ser.close()

    def __del__(self):
        self.stop()
        self.send_thread.stop()

    def startThread(self):
        self.send_thread.start()

    def loop(self):
        while True:
            self.send()

port = sys.argv[1]
channel_str = sys.argv[2]
channel_int = int(channel_str)
data = sys.argv[3]

dmx = DMX(port,Cnumber=channel_int)

dmx.start()

dmx.sendzero()

lighting_data_array = str(data).split(',')

pass_array = [0] * channel_int

for i in range(len(lighting_data_array)):
        pass_array[i] = int(lighting_data_array[i])

dmx.set_array(pass_array)

time.sleep(1000)