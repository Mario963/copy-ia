#!/usr/bin/python3
from GetUp import *
from Quadrapod import *

def main():
    quadrapod = Quadrapod()
    frontDist, backDist, rool, pitch = quadrapod.getSensorsValues()

    getUpModel = GetUp(quadrapod)

    init = tf.global_variables_initializer()
    saver = tf.train.Saver()

    # Run the session
    with tf.Session() as sess:
        sess.run(init) # Initialize variables

        if path.exists(modelSavePath + ".meta"):
            saver.restore(sess, modelSavePath)
        while True:
            getUpModel.executeLearningPeriod(sess)
            save_path = saver.save(sess, modelSavePath)
            quadrapod.printMotorsTemperatures()

if __name__ == "__main__":
    print("=== Quadrapod Learner ===")
    main()
