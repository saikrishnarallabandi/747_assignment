#!/usr/bin/python

import dynet as dy
import numpy as np
import pickle, os

class SaveableModel(object):
  
   def __init__(self, model):
     self.model = model

   def save(self, path):
     if not os.path.exists(path): os.makedirs(path)
     self.model.save(path, '/model')

   @staticmethod
   def load(model, path, load_model_params=True):
      if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
      with open(path + '/model', "r") as f: self.model = pickle.load(f)
      return self.model

class language_model(SaveableModel):
   
   def __init__(self, num_layers, num_input, num_hidden, model):
     self.num_layers = num_layers
     self.num_input = num_input
     self.num_hidden = num_hidden
     self.model = model
     self.RNN = dy.LSTMBuilder(self.num_layers, self.num_input, self.num_hidden, self.model)

   def get_LM(self):
     return self.RNN
   
   def get_model(self):
     return self.model

   def save(self, path):
     if not os.path.exists(path): os.makedirs(path)
     arr = [ self.num_layers, self.num_input, self.num_hidden ]
     self.model.save(path + '/model')
     with open(path + '/model_hyps', 'w') as f: pickle.dump(arr, f) 

   def print_params(self):
      print self.num_layers
      print self.num_input
      print self.num_hidden

   def load_model(self, model, path):
      model.populate(path + '/model')
      with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
      self.model = model
      self.num_layers = arr[0]
      self.num_input = arr[1]
      self.num_hidden = arr[2]

   def load_copy(self, model, path):
       if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
       with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
       model.populate(path + '/model')
       return model

   @staticmethod
   def load(model, path):
       if not os.path.exists(path): raise Exception("Model "+path+" does not exist")
       with open(path+"/model_hyps", "r") as f: arr = pickle.load(f)
       model.populate(path + '/model')
       return model
   
   def calculate_LM_loss(sequence):
      
      # Renew the computation graph
      dynet.renew_cg()
 
      # Initialize the RNN
      f_init = self.RNN.initial_state()



m = dy.Model()
A = language_model(1,128,256,m)
A.save("test_LM.save")
A.print_params()

m2 = dy.Model()
B = language_model(1,128,256,m2)
B.load_model(m, 'test_LM.save')
B.print_params()



