#include "infection_classes.h"
#include <random>
#include <vector>
#include <string>
#include <ctime>
#include <sstream>
#include <fstream>
#include <numeric>

using std::srand;
using std::vector;
using std::string;
using std::to_string;
using std::stringstream;
using std::time;
using std::ofstream;
using std::accumulate;

void write_data(stringstream &my_data, float infectivity,
                 float min_vaccination_rate){
    my_data << infectivity << "," << 
    min_vaccination_rate << '\n';
}

void save_data(stringstream const &my_data){
    string file_name = "1_SIR_sim_herd_immunity.csv" ;
    ofstream output_file;
    output_file.open (file_name);
    output_file << my_data.str();
    output_file.close();
}

float average(vector<float> data){
    float mean = accumulate(data.begin(), data.end(), 0.0) / (1.0 * data.size());
    return mean;
}

int main(){
srand(time(0));
int population_total = 50000; // number of people per simulation
int infection_time = 6; //number of days people can be infected for
int meetings_per_day = 4; //number of people met by infected per day
int initial_infected = 5; //number of people initially infected
int number_trials = 3; //number of trials we run each experiment for
stringstream data;
    data << "infectivity" << "," << "vaccination_rate" << "\n" ;
    for (float infectivity = 0.0; infectivity <= 1; infectivity += 0.01){
        vector<float> all_req_vaccines(number_trials);
        for (int infection_trial = 0.0; infection_trial < number_trials; infection_trial++){
            for (float vacc_rate = 0.0; vacc_rate < 0.9991; vacc_rate += 0.01){
                vector<float> all_vuln_safe(number_trials);
                for (int vacc_trial = 0; vacc_trial < number_trials; vacc_trial++){
                    population ut_campus(population_total, infectivity, vacc_rate, infection_time, 1, meetings_per_day);
                    for (int patient_zero = 0; patient_zero < initial_infected; patient_zero++){
                        ut_campus.infect_random();
                    }
                    int initial_vuln_safe = ut_campus.count_vulnerable();
                    while (ut_campus.count_infected() > 0){
                        ut_campus.update();
                    }
                    int final_vuln_safe = ut_campus.count_vulnerable();
                    float frac_vuln_safe = (1.0 * final_vuln_safe) / initial_vuln_safe;
                    all_vuln_safe[vacc_trial] = (frac_vuln_safe);
                }

                if (average(all_vuln_safe) > 0.95){
                    all_req_vaccines[infection_trial] = (vacc_rate);
                    break;
                }
            }
            
        }
    write_data(data, infectivity, average(all_req_vaccines));
}
save_data(data);
return 0;
}




