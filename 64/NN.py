from fann2 import libfann
import numpy as np

class NeuralNet:

    def __init__(self):
        pass

    def new_net(self):
        num_input = 128 # 32 piece locations for white(x2 man/king), 32 for black(x2 man/king), net always assumes its your turn
        num_output = 1 # valuation of a particular move
        num_hidden = 64 # quick rule of thumb judgement: hidden = mean(input, output)
        self.ann = libfann.neural_net()
        self.ann.create_standard_array((num_input,num_hidden,num_output))
        self.ann.set_learning_rate(.1)
        self.ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
        self.ann.randomize_weights(-.1,.1)

    def random(self):
        self.ann.randomize_weights(-.1,.1)

    def run(self,input_vector):
        return self.ann.run(input_vector)

    def train(self,input,desired_output):
        self.ann.train(input,[desired_output])

    def save(self,filename):
        self.ann.save(filename)

    def load(self,filename):
        self.ann = libfann.neural_net()
        self.ann.create_from_file(filename)