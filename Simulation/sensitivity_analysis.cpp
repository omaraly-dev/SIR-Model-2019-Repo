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
using std::ifstream;
using std::getline;
using std::stof;
using std::accumulate;

float average(vector<float> data){
    float mean = accumulate(data.begin(), data.end(), 0.0) / (1.0 * data.size());
    return mean;
}


vector<float> read_input(string filename){
    ifstream file(filename);
    string line;
    std::string::size_type size_thing;
    vector<float> input_data;
    while(getline(file, line)){
        input_data.push_back(stof(line, &size_thing));
    }
    return input_data;
}

void write_data(stringstream &my_data, float value){
    my_data << value << '\n';
}

void save_data(stringstream const &my_data, string filename){
    ofstream output_file;
    output_file.open (filename);
    output_file << my_data.str();
    output_file.close();
}


int main() {

srand(time(0));
int population_total = 50000; // number of people per simulation
int infection_time = 6; //number of days people can be infected for
int meetings_per_day = 4; //number of people met by infected per day
int initial_infected = 5; //number of people initially infected
int number_trials = 10; //number of trials we run each experiment for
float increments = 0.5/100; //how much vaccination rate and infectivity increment

string infectivity_input = "opt_infectivities.txt", vacc_rate_input = "opt_vacc_rates.txt";
stringstream disease_lifetimes, frac_vuln_safe;

vector<float> infectivities = read_input(infectivity_input), 
                    vacc_rates = read_input(vacc_rate_input);

for (int index = 0; index < infectivities.size(); index++){

    vector<float> vuln_safe(number_trials), lifetimes(number_trials);
    float infectivity = infectivities[index];
    float vacc_rate = vacc_rates[index];

    for (int trial = 0; trial < number_trials; trial++){
        population ut_campus(population_total, infectivity, vacc_rate, infection_time, 1, meetings_per_day);
        for (int patient_zero = 0; patient_zero < initial_infected; patient_zero++){
            ut_campus.infect_random();
        }
        int initial_vuln = ut_campus.count_vulnerable(), days = 0;
        
        while(ut_campus.count_infected() > 0){
            ut_campus.update();
            days++;
        }
        int final_vuln = ut_campus.count_vulnerable();
        lifetimes[trial] = days * 1.0; //need to do this to use avg function, loss of precision is marginal at best
        vuln_safe[trial] = (1.0 * final_vuln) / initial_vuln;
    }
    write_data(disease_lifetimes, average(lifetimes));
    write_data(frac_vuln_safe, average(vuln_safe));
}
save_data(disease_lifetimes, "disease_lifetimes.csv");
save_data(frac_vuln_safe, "frac_vuln_safe.csv");

}