import tensorflow as tf
import numpy as np
from os import path
from settings import *

class MotorsANN:
    def __init__(self):
        self.entry = tf.placeholder(tf.float32, shape=[None, nbEntry])
        # Construct neural network
        self.hiddens = []
        for i, it in enumerate(nbHiddens):
            self.hiddens.append(tf.layers.dense(self.entry if i == 0 else \
                                                self.hiddens[-1], it, activation=tf.nn.selu))
        self.out = tf.layers.dense(self.hiddens[-1], nbOutput)
        # Actions taken randomly with output layers probabilities
        self.actionLearning = tf.multinomial(tf.log(tf.nn.softmax(self.out)), num_samples=1)
        # Taken actions are outputs argmax
        self.action = tf.argmax(self.out, axis=1)

        self.y = tf.placeholder(tf.int32, shape=[1]) # Expected activations
        self.xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=self.out, labels=self.y) # Loss

        self.optimizer = tf.train.AdamOptimizer(learning_rate=learningRate)
        self.grad_and_vars = self.optimizer.compute_gradients(self.xentropy) # Compute gradients
        self.gradients = [] # Gradient of neural network. To evaluate to compute gradients

        self.current_gradients = [] # Gradients of actual try
        self.all_gradients = [] # Gradients of all tries

        self.gradient_placeholders = [] # Array of placeholders for gradients
        self.grad_and_vars_feed = [] # Array that will feed the optimizer with computed gradients
        for grad, var in self.grad_and_vars:
            if (grad != None):
                self.gradients.append(grad) # Add gradient computation tensor
                # Placeholder and feed dict for optimizer gradient feeding
                tmp_placeholder = tf.placeholder(tf.float32, shape=grad.get_shape())
                self.gradient_placeholders.append(tmp_placeholder)
                self.grad_and_vars_feed.append((tmp_placeholder, var))

        self.training_op = self.optimizer.apply_gradients(self.grad_and_vars_feed)

        # Feed dictionary to give to the optimizer
    def getGradientFeed(self, gradients, all_rewards):
        feed_dict = {}
        for grad_idx, grad_placeholder in enumerate(self.gradient_placeholders):
            tmp_grad = [] # Gradient * Reward
            for try_index, rewards in enumerate(all_rewards): # For each try
                for step, reward in enumerate(rewards): # For each step in current try
                    tmp_grad.append(reward * gradients[try_index][step][grad_idx]) # Gradient * reward
            mean_gradients = np.mean(tmp_grad, axis=0) # Mean gradients
            feed_dict[grad_placeholder] = mean_gradients
        return feed_dict

    def newTry(self):
        self.all_gradients.append(self.current_gradients)
        self.current_gradients = []

    def takeLearningAction(self, session, obs):
        a = session.run(self.actionLearning, feed_dict={self.entry: [obs]})[0] # Get action
        grads = session.run(self.gradients, feed_dict={self.entry: [obs], self.y: a}) # Get gradients
        self.current_gradients.append(grads) # Save gradient
        return a[0]

    def takeAction(self, session, obs):
        return session.run(self.action, feed_dict={self.entry: [obs]})

    def applyGradients(self, session, all_rewards):
        feed_dict = self.getGradientFeed(self.all_gradients, all_rewards)
        # Execute policy gradient descent
        session.run(self.training_op, feed_dict=feed_dict)
        self.current_gradients = []
        self.all_gradients = []
