from math import sqrt
from math import fabs
from random import randint
import numpy as np
from settings import *

class GetUpEnvironment:
    def __init__(self, quadrapod):
        self.quadrapod = quadrapod
        self.step = 0

    def getObs(self):
        out = [self.quadrapod.getMotorPosition(id) for id in allMotorsIds]
        return np.array(out)

    def reset(self):
        self.step = 0
        for i, it in enumerate(allMotorsIds):
            if (i % 3) == 0: # Coxa
                target = randint(0, nbMove - 1)
            elif (i % 3) == 1: # Femur
                target = 0
            else: # Tibia
                target = nbMove - 1
            self.quadrapod.moveMotor(it, target / nbMove, 100)
        self.quadrapod.waitMotorsStopped()
        return self.getObs()

    def executeStep(self, action):
        reward = 0.
        done = False

        if self.step == nbStepPerTry:
            done = True

        motorIdx = int(action / nbMove)
        pos = action % nbMove

        if motorIdx < nbMotor:
            self.quadrapod.moveMotor(allMotorsIds[motorIdx], pos / nbMove, motorSpeed)

        frontDist, backDist, roll, pitch = self.quadrapod.getSensorsValues()
        reward -= fabs(17 - frontDist)
        reward -= fabs(17 - backDist)
        reward -= fabs(roll * gyroRewardCoeff)
        reward -= fabs(pitch * gyroRewardCoeff)

        self.step += 1

        obs = self.getObs()
        return obs, reward, done
