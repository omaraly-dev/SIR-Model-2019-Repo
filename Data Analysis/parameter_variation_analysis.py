#script to process data from my examination of the system's end state
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
from mpl_toolkits.mplot3d import Axes3D



fig_dims = 15
aspect_ratio = 4/3
fig_dpi = 400
fig_font = 16
font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : fig_font}
mpl.rc('font', **font)


filename = "SIR_sim_sensitivity_data.csv"
filepath = r"C:\\Users\Omar\Desktop\sds proj infection\sensitivity data\extra\ "[:-1]
data = pd.read_csv(filepath + filename)
data_types = ["trial", "infectivity", "vacc_rate", "vuln_safe", "end_time"]
number_trials = 50

infectivity = data[data_types[1]].to_numpy()
vacc_rate = data[data_types[2]].to_numpy()
vuln_safe = data[data_types[3]].to_numpy()
end_time = data[data_types[4]].to_numpy()

data_points = infectivity.size
average_data_points = int(data_points / number_trials)
average_data = np.zeros((average_data_points, 4)) # stores averaged data in order of their definitions earlier


infectivity = np.reshape(infectivity, (data_points, 1))
vacc_rate = np.reshape(vacc_rate, (data_points, 1))
vuln_safe = np.reshape(vuln_safe, (data_points, 1))
end_time = np.reshape(end_time, (data_points, 1))


for avg_index, index in zip(range(average_data_points), range(0, data_points, number_trials)):
    average_data[avg_index, 0:2] = np.asarray([infectivity[index, 0], vacc_rate[index, 0]])
    average_data[avg_index, 2:] = np.mean(np.concatenate((vuln_safe[index : index + number_trials], 
                                    end_time[index : index + number_trials]), axis=1), axis=0)





# exporting data and plotting

np.savetxt(filepath + 'averaged_simulation_data.csv', average_data, header=','.join(data_types[1:]), delimiter=',')

grid_shape = (np.unique(average_data[:, 0]).size, np.unique(average_data[:, 1]).size)

infect_mesh = np.reshape(average_data[:, 0], grid_shape) * 100
vacc_mesh = np.reshape(average_data[:, 1], grid_shape) * 100
avg_vuln_safe = np.reshape(average_data[:, 2], grid_shape) * 100
avg_infection_life = np.reshape(average_data[:, 3], grid_shape)


# plotting
axis_labels = ['Infection Probability (%)', 'Percent of Population Vaccinated', 
                'Average Disease Lifetime (days)', 'Percent of Vulnerable Population Uninfected']

figure = plt.figure()
figure.set_figheight(fig_dims / aspect_ratio)
figure.set_figwidth(fig_dims)

ax = plt.axes(projection='3d')


ax.plot_surface(infect_mesh, vacc_mesh, avg_infection_life, cmap='plasma', edgecolor='none')
ax.set_xlabel(axis_labels[0])
ax.set_ylabel(axis_labels[1])
ax.set_zlabel(axis_labels[2])
plt.title("Disease Lifetime Parameter Study")
plt.savefig("lifetime.png")
plt.close()

figure = plt.figure()
figure.set_figheight(fig_dims / aspect_ratio)
figure.set_figwidth(fig_dims)

ax = plt.axes(projection='3d')

ax.plot_surface(infect_mesh, vacc_mesh, avg_vuln_safe, cmap='viridis', edgecolor='none')
ax.set_xlabel(axis_labels[0])
ax.set_ylabel(axis_labels[1])
ax.set_zlabel(axis_labels[3])
plt.title("Herd Immunity Parameter Study")
plt.savefig("herd_immunity.png", bbox_inches='tight', pad_inches=0.3, dpi=fig_dpi)
plt.close()

interest_infectivities = [0.2, .6, 1]
figure, ax = plt.subplots()

colors = ['xkcd:azure', 'xkcd:dark rose', 'xkcd:seafoam']
for interest_index, color_thing in zip(interest_infectivities, colors):
        index = int(interest_index*40000)
        line_label = 'Infection Probability = ' + str(interest_index * 100)  +'%'
        ax.plot(average_data[index:index+200,1], average_data[index:index+200,3], label=line_label, color=color_thing)
plt.xlabel('Percent of Population Vaccinated')
plt.ylabel('Disease Lifetime (days)')
plt.legend(loc=2, prop={'size': int(fig_font * 3/4)})
plt.savefig('2d slice lifetime plot.png')
plt.close()

figure = plt.figure()
figure.set_figheight(fig_dims / aspect_ratio)
figure.set_figwidth(fig_dims)

ax = plt.axes(projection='3d')


ax.contour3D(infect_mesh, vacc_mesh, avg_infection_life)
ax.set_xlabel(axis_labels[0])
ax.set_ylabel(axis_labels[1])
ax.set_zlabel(axis_labels[2])
plt.title("Disease Lifetime Parameter Study")
plt.savefig("lifetime contour.png")
plt.close()

