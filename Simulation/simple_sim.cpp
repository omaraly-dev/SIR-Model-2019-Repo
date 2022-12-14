#include "infection_classes.h"
#include <iomanip>
#include <random>
#include <vector>
#include <string>
#include <ctime>
#include <sstream>
#include <fstream>

using std::srand;
using std::vector;
using std::string;
using std::stringstream;
using std::time;
using std::ofstream;
using std::setprecision;
using std::fixed;

void write_data(stringstream &my_data, string system_data, int system_time){
    my_data << system_data << "," << system_time << '\n';
}

void save_data(stringstream const &my_data, float infectivity, float vaccination_rate, int simulation_type, int trial_number){
    stringstream file_name ;
    file_name << "SIR_sim_" << std::fixed << std::setprecision(2) << infectivity << "_" << vaccination_rate << "_" 
                        << simulation_type << "_" << trial_number << ".csv";
    ofstream output_file;
    output_file.open (file_name.str());
    output_file << my_data.str();
    output_file.close();
}

int main(){
srand(time(0));
vector<float> infectivities{ 0.2,  0.4,  0.6, 0.8, 0.9},
              vaccination_rates{0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99};
int population_total = 50000; // number of people per simulation
int infection_time = 6; //number of days people can be infected for
int meetings_per_day = 8; //number of people met by infected per day
int initial_infected = 5; //number of people initially infected
int number_trials = 3; //number of trials we run each experiment for
for (float infectivity : infectivities){
    for (float vaccination_rate : vaccination_rates){
        for (int simulation_type = 1; simulation_type < 4; simulation_type++){
            for (int trial = 0; trial < number_trials; trial++){
                population
                    ut_campus(population_total, infectivity, vaccination_rate, infection_time, simulation_type, meetings_per_day);
                    for(int patient_zeros = 0; patient_zeros < initial_infected; patient_zeros++){
                        ut_campus.infect_random();
                    }
                    int days = 0;
                    stringstream data;
                    data << "system_data" << "," << "system_time" << "\n" ;
                    write_data(data, ut_campus.population_breakdown(), days);
                    while (ut_campus.count_infected() > 0){
                        ut_campus.update();
                        days++;
                        write_data(data, ut_campus.population_breakdown(), days);
                    }
                    save_data(data, infectivity, vaccination_rate, simulation_type, trial);

            }
        }
    }
}
return 0;
}
