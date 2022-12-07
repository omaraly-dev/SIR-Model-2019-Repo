#script to do the herd immunity analysis
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl
import scipy.optimize as opt 

def fit_function(infectivity):
    v = 1 - 1 / (infectivity ) / (4 * 6)
    return v * 100	

fig_dims = 15
aspect_ratio = 4/3
fig_dpi = 400
fig_font = 16
font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : fig_font}
mpl.rc('font', **font)

filename = 'herd_immunity.csv'

data = np.genfromtxt(filename, delimiter=',', names=True)

figure, ax = plt.subplots()

figure.set_figheight(fig_dims / aspect_ratio)
figure.set_figwidth(fig_dims)


ax.plot(data['infectivity']*100, data['vaccination_rate']*100, color='xkcd:watermelon', label='Simulation Data')
plt.xlabel("Disease Infection Probability (%)")
plt.ylabel("Minimum Vaccination Rate for Herd Immunity (%)")
plt.xlim(0,100)
plt.ylim(0,100)
plt.title('herd immunity plot')
plt.savefig('min_herd_immunity.png', bbox_inches='tight', pad_inches=0.3, dpi=fig_dpi)
plt.close()

reproduction_number = data['infectivity'] * 4 * 6



figure, ax = plt.subplots()

figure.set_figheight(fig_dims / aspect_ratio)
figure.set_figwidth(fig_dims)
ax.plot(reproduction_number, fit_function(data['infectivity']), 
                label='Fit Function', color='xkcd:cornflower')
ax.plot(reproduction_number, data['vaccination_rate']*100,'o', color='xkcd:watermelon', label='Simulation Data')
plt.xlabel("Basic Reproduction Number $R_0$")
plt.ylabel("Minimum Vaccination Rate for Herd Immunity (%)")
plt.xlim(reproduction_number[0],reproduction_number[-1])
plt.ylim(0,100)
plt.title('herd immunity plot')
plt.legend()
plt.savefig('min_herd_immunity_fit.png', bbox_inches='tight', pad_inches=0.3, dpi=fig_dpi)

