# QuadrapodLearner
A program that learn how to control a quadrapod robot using Deep Reinforcement Learning algorithm (QLearning algorithm using Artificial Neural Network)

- Step 1: Learn how to stand up;
- Step 2: Learn how to turn right / left;
- Step 3: Learn how to walk;
- Step 4: Discover an environment.

## Quadrapod Details

- Structure Material: Plexiglas;
- Servo-Motor: Dynamixel AX-12A;
- Battery: Zippy8000 30C Serie;
- NbLegs = 4;
- NbMotorPerLegs = 3;
- NbMotor = NbLegs * NbMotorPerLegs = 3 * 4 = 12;
- Controler: Raspberry Pi 3.

### Sensors

- 2 Ultrasonics sensors (HC-SR04): pointing to the ground, it allow us to know the distance from the ground;
- 1 myAHRS+ (Attitude Heading Reference System): his 3-axis 16-bit gyroscope allow us to know the body orientation.

## Algorithm Details

- Programming language: Python 3.5;
- Gradient Politic Algorithm;
- This algorithm is consistent with the Markov decision process and allow the agent to improve his performances by testing his politic.

## Artificial Neural Network Details

- Used library: Tensorflow
- Number of layer: 3
- Layer 1 (entry layer): nbMotor = 12
- Layer 2 (hidden layer): 24 neurons (RELU activation function)
- Layer 3 (output layer): nbMotor * nbAction = 12 * 3 = 36 (Linear activation function)
- Learning Rate: 0.01

## Research Links

- [Distral: Robust Multitask Reinforcement Learning](https://arxiv.org/abs/1707.04175)
