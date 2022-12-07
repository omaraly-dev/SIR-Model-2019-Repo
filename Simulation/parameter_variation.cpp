#include "infection_classes.h"
#include <random>
#include <vector>
#include <string>
#include <ctime>
#include <sstream>
#include <fstream>

using std::srand;
using std::vector;
using std::string;
using std::to_string;
using std::stringstream;
using std::time;
using std::ofstream;



void write_data(stringstream &my_data, float infectivity, int trial_number,
                 float vaccination_rate, float fraction_vulnerable_uninfected, int end_time){
    my_data << trial_number << "," << infectivity << "," << 
    vaccination_rate << "," << fraction_vulnerable_uninfected  << "," << end_time << '\n';
}

void save_data(stringstream const &my_data){
    string file_name = "SIR_sim_sensitivity_data.csv";
    ofstream output_file;
    output_file.open (file_name);
    output_file << my_data.str();
    output_file.close();
}


int main() {

srand(time(0));
int population_total = 50000; // number of people per simulation
int infection_time = 6; //number of days people can be infected for
int meetings_per_day = 4; //number of people met by infected per day
int initial_infected = 5; //number of people initially infected
int number_trials = 50; //number of trials we run each experiment for
float increments = 0.5/100; //how much vaccination rate and infectivity increment

stringstream data;
data << "trial,infectivity,vacc_rate,vuln_safe,end_time\n";

for (float infectivity = 0; infectivity <= 1; infectivity += increments){
    for(float vaccination_rate = 0; vaccination_rate <= 0.995; vaccination_rate += increments){
        for (int trial = 0; trial < number_trials; trial++){
            population ut_campus(population_total, infectivity, vaccination_rate, infection_time, 1, meetings_per_day);

            for (int patient_zeros = 0; patient_zeros < initial_infected; patient_zeros++){
                ut_campus.infect_random();
            }

            int days = 1;

            int initial_num_vuln = ut_campus.count_vulnerable();
            
            while (ut_campus.count_infected() > 0){
                ut_campus.update();
                days++;
            }

            int final_num_vuln = ut_campus.count_vulnerable();
            float fraction_safe = final_num_vuln * 1.0 / initial_num_vuln;
            write_data(data, infectivity, trial, vaccination_rate, fraction_safe, days);

        }
    }
}
save_data(data);
}