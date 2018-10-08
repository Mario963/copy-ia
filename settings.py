# Reinforcement Learning

#       Environement
nbStepPerTry = 50
nbTrain = 500 # Maximum train epoch
nbTryPerTrain = 5 # Number of try each epoch
punishLosses = True
discountRate = 0.5
gyroRewardCoeff = 0.25

#       Quadrapod properties
nbLeg = 4 # 2 front legs and 2 back legs
nbMotorPerLeg = 3
nbMotor = nbLeg * nbMotorPerLeg
maxMotorAngle = 90 # Limit motors to 90 degree angle
nbMove = 5 # Number of step that the quadrapod have to execute to reach 90 degree
initialPosFilename = "motorPos.conf"
myAHRS_plusPath = "/dev/ttyACM0"
dxlPath = "/dev/ttyACM1"

#       Motors
frontRightIds = [10, 11, 12] # Coxa, femur, tibia
frontLeftIds = [20, 21, 22]
backLeftIds = [30, 31, 32]
backRightIds = [40, 41, 42]
allMotorsIds = frontRightIds + frontLeftIds + backRightIds + backLeftIds

frontRightDirs = [-1., 1., -1] # Coxa, femur, tibia
frontLeftDirs = [1., 1., -1]
backRightDirs = [1., 1., -1]
backLeftDirs = [-1., 1., -1]
motorsDirs = frontRightDirs + frontLeftDirs + backRightDirs + backLeftDirs

motorAngle = 300 # From 0 to 300 degree
nbMotorStep = 1024 # Possibles positions
motorSpeed = 800
motorTorque = 1023

#               Fixed limits
moveSize = (nbMotorStep * maxMotorAngle) / motorAngle # Number of step with 90 angle

#       Sensors
frontDistPins = [23, 24] # Trigger, Echo
backDistPins = [8, 7]

#       Neural network
nbEntry = nbMotor
nbHiddens = [30, 50, 30]
nbOutput = (nbMotor * nbMove) + 1 # All motor actions + wait action
modelSavePath = "./trainSave/model.ckpt"
modelLogPath = "logs/getUp"
learningRate = 1e-2
