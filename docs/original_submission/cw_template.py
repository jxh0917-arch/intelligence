#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7CCEMIAA Intelligence and Autonomy

Coursework 1: Chameleon's Tongue
"""
import math
import random
import numpy as np
import sklearn.linear_model
import sklearn.neural_network 
import sklearn.metrics
from chameleon import chameleon
# ---- DO NOT MODIFY ABOVE THIS LINE ---- #
def estimate_model(R,Q):
	model = sklearn.neural_network.MLPRegressor()
# ---- Begin Answer to Question 1 ---- #

# ---- End Answer to Question 1 ---- #
	return model

def estimate_rmse(Rd,model):
	rmse = -1 # initialise return value
# ---- Begin Answer to Question 2 ---- #

# ---- End Answer to Question 2 ---- #
	return rmse

def estimate_probability(Rd,model):
	probability = -1 # initialise return value
# ---- Begin Answer to Question 3 ---- #

# ---- End Answer to Question 3 ---- #
	return probability

def estimate_mass(Q,Qdot,Qddot,Tau):
	mass = -1 # initialise return value
# ---- Begin Answer to Question 4 ---- #

# ---- End Answer to Question 4 ---- #
# ---- DO NOT MODIFY BELOW THIS LINE ---- #
	return mass

def main():
	random.seed(1)
	np.random.seed(1)

	# load training data
	R     = np.loadtxt('R.csv'    ,  delimiter=',') # tongue tip locations
	Q     = np.loadtxt('Q.csv'    ,  delimiter=',') # tongue configurations (angle and length)
	Qdot  = np.loadtxt('Qdot.csv' , delimiter=',') # tongue velocities
	Qddot = np.loadtxt('Qddot.csv', delimiter=',') # tongue accelerations
	Tau   = np.loadtxt('Tau.csv'  , delimiter=',') # tongue generalised forces
	Rd    = np.loadtxt('Rd.csv'   , delimiter=',') # insect locations
	Rp    = np.full(Rd.shape,math.nan) # initialise an array of NaNs

	# estimate model
	model = estimate_model(R,Q)

	# compute RMSE in model
	rmse = estimate_rmse(Rd,model)

	# compute probability of catching prey
	probability = estimate_probability(Rd,model)

	# estimate mass of tongue
	mass = estimate_mass(Q,Qdot,Qddot,Tau)
if __name__ == "__main__":
    main()
