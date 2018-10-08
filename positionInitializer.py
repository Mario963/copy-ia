#!/usr/bin/python3
from dxl.dxlchain import DxlChain
from settings import *
import logging

# Save and restore motors positions when the robot is flat (initial pos)

def saveInitialMotorsPositions(chain):
    file = open(initialPosFilename, "w")
    for id in allMotorsIds:
        file.write(str(chain.get_reg(id, "present_position")) + "\n")
    file.close()

def getInitialMotorsPositions():
    out = []
    file = open(initialPosFilename, "r")
    for line in file.readlines():
        if line != "":
            out.append(float(line))
    file.close()
    return (out)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    chain = DxlChain(dxlPath, rate=1000000)

    chainIds = chain.get_motor_list() # Get chain ids
    print(chainIds)
    # Check if all needed motors are in the chain
    for motor in allMotorsIds:
        if not motor in chainIds:
            raise ValueError("{}: motor not found in chain".format(motor))
    saveInitialMotorsPositions(chain)
