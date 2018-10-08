from dxl.dxlchain import DxlChain
from myAHRS_plus import *
from DistanceSensor import *
from positionInitializer import getInitialMotorsPositions
import logging
from time import sleep
from settings import *

class Quadrapod:
    def __init__(self):
        self.initMotors()
        self.initSensors()

    def initMotors(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        self.chain = DxlChain(dxlPath, rate=1000000, timeout=0.5)

        self.lastMotorsPos = {}
        chainIds = self.chain.get_motor_list() # Get chain ids
        # Check if all needed motors are in the chain
        for motor in allMotorsIds:
            if not motor in chainIds:
                raise ValueError("{}: motor not found in chain".format(motor))
            self.lastMotorsPos[motor] = 0.

        self.initMotorsSpeedAndTorque()
        self.initMotorsBounds()

    def initMotorsSpeedAndTorque(self):
        for id in allMotorsIds:
            self.chain.set_reg(id, "moving_speed", motorSpeed)
            self.chain.set_reg(id, "max_torque", motorTorque)
            self.chain.set_reg(id, "torque_limit", 1023)

    def initMotorsBounds(self):
        self.motorsBounds = {}
        for i, it in enumerate(getInitialMotorsPositions()):
            id = allMotorsIds[i]
            if motorsDirs[i] == -1:
                self.motorsBounds[id] = [it - moveSize, it]
            elif motorsDirs[i] == 1:
                self.motorsBounds[id] = [it, it + moveSize]

    def initSensors(self):
            self.myAHRS = myAHRS_plus(myAHRS_plusPath)
            self.frontDistSensor = DistanceSensor(frontDistPins[0], frontDistPins[1])
            self.backDistSensor = DistanceSensor(backDistPins[0], backDistPins[1])

    def printMotorsTemperatures(self):
        print("Motors temperatures:")
        for motor in allMotorsIds:
            try:
                temp = self.chain.get_reg(motor, "present_temp")
                print("{}: {} degree celsus".format(motor, temp))
            except:
                print("{}: Cannot get temperature".format(motor))

    # Move motor to given position (between 0 and 1)
    def moveMotor(self, id, pos, speed=None):
        pos = self.motorsBounds[id][0] + (pos * moveSize)
        if pos < 0:
            pos = 0
        elif pos > nbMotorStep:
            pos = nbMotorStep - 1

        try:
            self.chain.goto(id, pos, speed, False)
        except:
            print(id)
            print("Move motor exception")
            pass

    def waitMotorsStopped(self):
        try:
            self.chain.wait_stopped(allMotorsIds)
        except:
            print("wait motor exception")
            sleep(0.5)

    # Get motor position between 0 and 1
    def getMotorPosition(self, id):
        try:
            pos = self.chain.get_reg(id, "present_position")
            self.lastMotorsPos[id] = (pos - self.motorsBounds[id][0]) / moveSize
            return self.lastMotorsPos[id]
        except:
            print(id)
            print("Get motor exception")
            return self.lastMotorsPos[id]

    def getSensorsValues(self):
        frontDist = self.frontDistSensor.getDistance()
        backDist = self.backDistSensor.getDistance()
        data = self.myAHRS.getValues()
        roll = data[1]
        pitch = data[2]
        return frontDist, backDist, roll, pitch
