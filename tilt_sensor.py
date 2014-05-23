
import math
import serial

class Lpf:
    def sinc(self, x):
        if x == 0.0: return 1.0
        else: return math.sin(x) / x

    def __init__(self, fc, delta):
        self.n = round(3.1 / delta) - 1
        if (self.n + 1) % 2 == 0: self.n += 1
        self.n = int(self.n)
        
        self.b = []
        for i in range(-self.n / 2, self.n / 2 + 1):
            self.b.append(2.0 * fc * self.sinc(2.0 * math.pi * fc * i))
        self.x = [0.0] * (self.n + 1)
        
        for i in range(len(self.b)):
            self.b[i] *= 0.54 - 0.46 * math.cos(2 * math.pi / len(self.b) * i)

    def filter(self, input):
        self.x.append(input)
        self.x.pop(0)
        y = 0
        for i in range(self.n + 1):
            y += self.b[i] * self.x[self.n - i]
        return y

class Hpf:
    def sinc(self, x):
        if x == 0.0: return 1.0
        else: return math.sin(x) / x

    def __init__(self, fc, delta):
        self.n = round(3.1 / delta) - 1
        if (self.n + 1) % 2 == 0: self.n += 1
        self.n = int(self.n)
        
        self.b = []
        for i in range(-self.n / 2, self.n / 2 + 1):
            self.b.append(self.sinc(math.pi * i) - 2.0 * fc * self.sinc(2.0 * math.pi * fc * i))
        self.x = [0.0] * (self.n + 1)
        
        for i in range(len(self.b)):
            self.b[i] *= 0.54 - 0.46 * math.cos(2 * math.pi / len(self.b) * i)

    def filter(self, input):
        self.x.append(input)
        self.x.pop(0)
        y = 0
        for i in range(self.n + 1):
            y += self.b[i] * self.x[self.n - i]
        return y

class Accgyr:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud)
        self.acc = {'x' : 0, 'y' : 0, 'z' : 0}
        self.gyr = {'x' : 0, 'y' : 0, 'z' : 0}

    def get_data(self):
        d = self.ser.readline()
        d = d.strip('\n')
        d = d.split(' ')

        self.acc['x'] = int(d[0]) / 100
        self.acc['y'] = int(d[1]) / 100
        self.acc['z'] = int(d[2]) / 100
        self.gyr['x'] = int(d[3]) / 100
        self.gyr['y'] = int(d[4]) / 100
        self.gyr['z'] = int(d[5]) / 100

    def acc_tilt(self):
        d = []
        d.append(math.asin(self.acc['y'] / (math.sqrt(self.acc['y'] ** 2 + self.acc['z'] ** 2))) * (180 / math.pi))
        d.append(math.asin(self.acc['x'] / (math.sqrt(self.acc['x'] ** 2 + self.acc['z'] ** 2))) * (180 / math.pi))
        return d

if __name__ == '__main__' :
    obj = Accgyr(9, 19200)
    hpf = Hpf(10.0 / 200.0, 20.0 / 200.0)
    
    while True:
        obj.get_data()
        print obj.acc_tilt()
