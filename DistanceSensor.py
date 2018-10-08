import RPi.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, TRIGGER, ECHO):
        #GPIO Mode (BOARD / BCM)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        #set GPIO Pins
        self.GPIO_TRIGGER = TRIGGER
        self.GPIO_ECHO = ECHO

        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def getDistance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
            if StopTime - StartTime > 1.:
                break

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        if distance < 0. or distance > 1000.:
            return 0.
        return distance

if __name__ == "__main__":
    sensor = DistanceSensor(8, 7)
    sensor2 = DistanceSensor(23, 24)
    print(sensor.getDistance())
    print(sensor2.getDistance())
