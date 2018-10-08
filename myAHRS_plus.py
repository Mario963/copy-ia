import sys
import time 
import serial 
import traceback

class myAHRS_plus:
    def __init__(self, serial_device):
        self.serial_port = serial.Serial(serial_device, 115200, timeout=1.0)
        # Data transfer mode : ASCII, TRIGGER
        self.send_command('mode,AT')
        # Select output message type
        self.send_command('asc_out,RPYIMU')
    
    def send_command(self, cmd_msg):
        cmd_msg = '@' + cmd_msg.strip()
        crc = 0
        for c in cmd_msg:
            crc = crc^ord(c)
            self.serial_port.write((cmd_msg + '*%02X'%crc + '\r\n').encode())
            line = self.serial_port.readline().strip()
        return line

    def parse_data_message_rpyimu(self, data_message):
        # $RPYIMU,39,0.42,-0.31,-26.51,-0.0049,-0.0038,-1.0103,-0.0101,0.0014,-0.4001,51.9000,26.7000,11.7000,41.5*1F

        data_message = (data_message.decode("utf-8").split('*')[0]).strip() # discard crc field  
        fields = [x.strip() for x in data_message.split(',')]

        if(fields[0] != '$RPYIMU'):
                return None

        sequence_number, roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature = (float(x) for x in fields[1:])
        return (int(sequence_number), roll, pitch, yaw, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature)

    def getValues(self):
        line = self.send_command('trig')
        items = self.parse_data_message_rpyimu(line)
        return items
