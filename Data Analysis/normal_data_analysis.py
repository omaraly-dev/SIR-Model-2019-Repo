#script to analyze and plot the normal simulation results
import numpy as np 
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt 
import csv

def translate(system_string):
    number_vaccinated = system_string.count('#')
    number_recovered = system_string.count('-')
    number_infected = system_string.count('+')
    number_vulnerable = system_string.count('?')
    return np.asarray([number_vulnerable, number_infected, number_recovered, number_vaccinated])

def pull_data(csv_name):
    global column_names
    the_csv = pd.read_csv(csv_name)
    data_set = []
    for col in column_names:
        data_set.append(list(the_csv[col]))
    return data_set 

column_names = ['system_data', 'system_time']
base_name = 'SIR_sim'
infectivities = ['0.20', '0.40', '0.60', '0.80', '0.90']
vacc_rates = ['0.00', '0.20', '0.40', '0.60', '0.80', '0.90', '0.95', '0.90']
model_types = ['1', '2', '3']
trial_nums = ['0', '1', '2']
colors = ['xkcd:weird green', 'xkcd:lightish red', 'xkcd:ultramarine blue']
data_labels = ['Vulnerable', 'Infected', 'Recovered']
file_path = r'D:\sds proj infection\project submission\Simulation Data (processed and otherwise)\Baseline Simulations\Unprocessed Data\ '[:-1]
data_path = r'D:\sds proj infection\data\ '[:-1]
plot_path = r'D:\sds proj infection\sim_graphs\ '[:-1]
data_header = 'Time, Recovered, Infected, Vulnerable, Vaccinated'
fig_dims = 15
aspect_ratio = 4/3
fig_dpi = 400
fig_font = 24
font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : fig_font}

mpl.rc('font', **font)
population = 50000

for infectivity in infectivities:
    for vacc_rate in vacc_rates:
        for model_type in model_types:
            for trial_num in trial_nums:
                file_name = '_'.join([base_name, infectivity, vacc_rate, model_type, trial_num]) 
                data = pull_data(file_path + file_name + '.csv')
                system_status = data[0]
                number_points = len(data[1])
                time = np.asarray(data[1]).reshape((number_points,1))
                pop_stats = np.zeros((number_points, 4)) # Note, this stores rec_count, inf_count, vuln_count, vacc_count in THAT ORDER
                for status, index in zip(system_status, range(0, number_points)):
                    pop_stats[index, :] = translate(status)
                figure, ax = plt.subplots()
                figure.set_figheight(fig_dims / aspect_ratio)
                figure.set_figwidth(fig_dims)
                for index in range(0, 3):
                    ax.plot(time, 100 * pop_stats[:, index] / population, color=colors[index], label=data_labels[index])
                plt.xlabel('Time (days)')
                plt.ylabel('Percent of Population')
                plt.legend()
                plt.savefig(plot_path + file_name + '_plot.png', bbox_inches='tight', pad_inches=0.3, dpi=fig_dpi)
                plt.close()
                np.savetxt(data_path + file_name + '_data.csv', np.concatenate((time, pop_stats), axis=1), header=data_header, delimiter=',')

                








        

