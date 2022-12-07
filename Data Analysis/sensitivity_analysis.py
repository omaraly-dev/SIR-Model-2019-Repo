# sensitivity analysis data processing
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
from mpl_toolkits.mplot3d import Axes3D
from SALib.analyze import sobol
from SALib.sample import saltelli


problem = {
    'num_vars': 2,
    'names': ['infectivity', 'vaccination_rate'],
    'bounds': [[0.0, 1.0],
               [0.0, 0.995]]
}

test = saltelli.sample(problem, 1000) # I exported this separately, keeping it here for bookkeeping
lifetimes = np.loadtxt('disease_lifetimes.csv')
vuln_safe = np.loadtxt('frac_vuln_safe.csv')

analysis_lifetimes = sobol.analyze(problem, lifetimes)
print('lifetime analysis: ')
print('first-order sensitivity params: ', '\n', analysis_lifetimes['S1'])
print("infectivity-vacc rate interactions: ", analysis_lifetimes['S2'][0,1])

analysis_vuln_safe = sobol.analyze(problem, vuln_safe)
print('vulnerable population analysis: ')
print('first-order sensitivity params: ', '\n', analysis_lifetimes['S1'])
print("infectivity-vacc rate interactions: ", analysis_lifetimes['S2'][0,1])


