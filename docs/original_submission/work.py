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
	# We aim to learn the Inverse Kinematics mapping: Position (R) -> Joint Configuration (Q).
	# 1. hidden_layer_sizes=(200, 200): Increased capacity to capture complex kinematic non-linearities.
	# 2. activation='tanh': Smooth activation function suitable for continuous physical mappings.
	# 3. solver='lbfgs': An optimizer in the family of quasi-Newton methods, which converges betterand faster for small, noise-free datasets compared to 'adam'.
	# 4. max_iter=15000 & tol=1e-9: Ensure the solver runs long enough to reach high precision.
	model = sklearn.neural_network.MLPRegressor(
		hidden_layer_sizes=(200, 200),
		activation='tanh',
		solver='lbfgs',
		max_iter=15000,
		alpha=1e-7,  # Low regularization to allow precise fitting
		tol=1e-9,  # Strict tolerance for convergence
		random_state=1
	)

	# Fit the model.
	# Note: Inputs R and Targets Q are provided as (n_features, n_samples).
	model.fit(R.T, Q.T)
# ---- End Answer to Question 1 ---- #
	return model

def estimate_rmse(Rd,model):
	rmse = -1 # initialise return value
# ---- Begin Answer to Question 2 ---- #
	# 1. Transpose the target data to shape (n_samples, 2) for prediction.
	Rd_t = Rd.T

	# 2. Predict the necessary joint configurations (Q) to reach targets (Rd).
	Q_pred = model.predict(Rd_t)

	# 3. Use Forward Kinematics to map predicted angles back to Cartesian space (Position).
	# This allows us to compare the actual reached position vs the desired target.
	cham = chameleon()
	n_samples = Rd_t.shape[0]
	R_pred = np.zeros_like(Rd_t)

	for i in range(n_samples):
		R_pred[i] = cham.forward_kinematics(Q_pred[i])

	# 4. Calculate Mean Squared Error and then Root Mean Squared Error.
	mse = sklearn.metrics.mean_squared_error(Rd_t, R_pred)
	rmse = math.sqrt(mse)
# ---- End Answer to Question 2 ---- #
	return rmse

def estimate_probability(Rd,model):
	probability = -1 # initialise return value
# ---- Begin Answer to Question 3 ---- #
	# 1. Transpose input data.
	Rd_t = Rd.T

	# 2. Predict joint angles and compute resulting tip positions using Forward Kinematics.
	Q_pred = model.predict(Rd_t)
	cham = chameleon()
	n_samples = Rd_t.shape[0]
	R_pred = np.zeros_like(Rd_t)

	for i in range(n_samples):
		R_pred[i] = cham.forward_kinematics(Q_pred[i])

	# 3. Calculate Euclidean distance error for each sample.
	# axis=1 computes the norm across the coordinate dimension (x, y).
	errors = np.linalg.norm(Rd_t - R_pred, axis=1)

	# 4. Count successful catches.
	# A catch is successful if the tip is within the insect's radius (0.01m).
	success_count = np.sum(errors <= 0.01)

	# 5. Calculate probability as the ratio of successes to total attempts.
	probability = success_count / n_samples
# ---- End Answer to Question 3 ---- #
	return probability

def estimate_mass(Q,Qdot,Qddot,Tau):
	mass = -1 # initialise return value
# ---- Begin Answer to Question 4 ---- #
	# We rearrange the dynamics equations M(q)q_dd + C(q,q_d) + g(q) = Tau into linear form:
	# Phi * m = Tau, where 'm' is the unknown mass.

	# 1. Transpose all inputs to shape (n_samples, 1) or (n_samples, 2) to handle columns correctly.
	Q_t = Q.T
	Qdot_t = Qdot.T
	Qddot_t = Qddot.T
	Tau_t = Tau.T

	g = 9.81  # Acceleration due to gravity

	# 2. Extract state variables for clarity.
	q1 = Q_t[:, 0]
	q2 = Q_t[:, 1]
	qd1 = Qdot_t[:, 0]
	qd2 = Qdot_t[:, 1]
	qdd1 = Qddot_t[:, 0]
	qdd2 = Qddot_t[:, 1]
	tau1 = Tau_t[:, 0]
	tau2 = Tau_t[:, 1]

	# 3. Construct the regressor terms based on the provided Lagrangian dynamics equations.
	# Equation 1 (Torque): m * (q2^2 * qdd1 + 2*q2*qd2*qd1 + g*q2*cos(q1)) = tau1
	term1 = (q2 ** 2 * qdd1) + (2 * q2 * qd2 * qd1) + (g * q2 * np.cos(q1))

	# Equation 2 (Force): m * (qdd2 - q2*qd1^2 + g*sin(q1)) = tau2
	term2 = qdd2 - (q2 * qd1 ** 2) + (g * np.sin(q1))

	# 4. Stack data from both equations to form the full linear system X * m = y.
	X = np.concatenate([term1, term2])
	y = np.concatenate([tau1, tau2])

	# Reshape X to (n_samples, 1) to satisfy sklearn input requirements.
	X = X.reshape(-1, 1)

	# 5. Solve for mass 'm' using Linear Regression.
	# fit_intercept=False is required because the physics model (F=ma) passes through the origin.
	reg = sklearn.linear_model.LinearRegression(fit_intercept=False)
	reg.fit(X, y)

	mass = reg.coef_[0]
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