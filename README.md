# Clinic Simulation Model

A group student project for the Computer Simulation course: a discrete simulation of patient flow in an outpatient clinic, comparing scheduled appointments with walk-ins. It measures patient time, doctor idle time and overtime, and runs statistical tests and parameter sweeps.

## Requirements

- Python 3
- Dependencies listed in `requirements.txt` (numpy, scipy, pandas, matplotlib)

```bash
pip install -r requirements.txt
```

A Nix flake (`flake.nix`) is also provided for a reproducible environment:

```bash
nix develop
```

## File structure

- `src/main.py` – simple entry point that prints the results of both clinic variants.
- `src/distributions.py` – generation of arrival, registration and appointment time distributions, and of patient lists.
- `src/simulation.py` – core patient-flow simulation and functions that run the scenarios.
- `src/analysis.py` – statistical analysis module that runs repeated simulations, performs statistical tests and generates plots.

## Distribution generators (`distributions.py`)

- `get_walk_in_arrival_time_dist(num_patients, p_first=0.5)`
  Bimodal normal distribution of arrival times for walk-in patients (modes at minute 120 and minute 420, standard deviation of 90 minutes for both). Results are clipped to the clinic's opening hours.
- `get_arrival_offset(num_patients)`
  Skew-normal distribution of arrival offsets relative to the appointment time (mean -10, standard deviation 4, alpha 4, producing a right tail) for scheduled patients.
- `get_scheduled_arrival_time_dist(num_patients, num_doctors)`
  Creates arrival times every 20 minutes per consulting room, with the offset from the distribution above added.
- `get_registration_duration_dist(num_patients, multiplier)`
  Registration time is drawn from an exponential distribution with scale 1, multiplied by 1 for scheduled patients and 1.5 for walk-in patients (simulating longer registration when the clinic doesn't know the patient), and then 1 is added to eliminate zero values.
- `get_appointment_duration_dist(num_patients)`
  Appointment duration is drawn from a gamma distribution with shape 17 and scale 1, and 1 is added to the result.
- `get_scheduled_patients(num_patients, num_doctors)`
  Returns a list of scheduled patients sorted by arrival time: `(arrival_time, registration_time, appointment_time)` – ready-to-use simulation input.
- `get_run_walk_in_patients(num_patients)`
  Returns a list of walk-in patients sorted by arrival time – ready-to-use simulation input.

## Simulation core (`simulation.py`)

- `SimulationResult`
  Simple result aggregate: average total patient time (`avg_time`), overtime (`overtime`), lists of time spent in the clinic and time waiting for a doctor, and idle time per doctor (`idle_times`). Negative overtime means work finished early; positive means work after hours.
- `ClinicSimulation`
  Simulates patient flow:
  - registration: the patient picks the first free desk, waits or starts immediately;
  - consulting room: the patient picks the first free doctor; doctor idle time is summed;
  - metrics: total time (arrival → end of appointment) and time waiting for a doctor are recorded.
- `run_scheduled_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`
  Runs the simulation for patients with scheduled appointments and returns a `SimulationResult`.
- `run_walk_in_simulation(num_registration_desks=2, num_doctors=3, num_patients=100)`
  Runs the simulation for walk-in patients and returns a `SimulationResult`.

## Statistical analysis (`analysis.py`)

- `run_multiple_simulations(is_scheduled=True, runs=100, num_registration_desks=2, num_doctors=3, num_patients=85, verbose=True)`
  Runs repeated simulations and collects raw data: average patient times and overtime.

- `run_full_analysis(num_runs=100, num_registration_desks=2, num_doctors=3, num_patients=85, patients_range=range(10, 100, 10), doctors_range=range(1, 6))`
  Main function that runs the complete analysis.

- `calculate_statistics(data, name="")`
  Computes basic descriptive statistics for the given dataset: mean, median, standard deviation, minimum, maximum and percentiles (25%, 75%, 95%). Returns a dictionary of statistics.

- `z_test(data1, data2, name1="Z terminem", name2="Bez terminu", alpha=0.05)`
  Performs a Z-test for two independent samples. Computes the Z statistic, the p-value (two-sided test) and checks statistical significance at α=0.05. Returns a dictionary with the test results.

- `create_histogram_plot(data1, data2, ylabel, title_prefix, filename, color1='blue', color2='green', add_zero_line=False)`
  General-purpose function that creates a comparison histogram for two datasets (scheduled vs walk-in system). Optionally adds a reference line at 0 (for overtime).

- `create_comparison_plots(data_scheduled, data_walk_in)`
  Creates the full set of comparison plots:
  - Histograms of average patient time for both systems
  - Histograms of overtime for both systems (with a y=0 reference line)
  - Comparison boxplots for both metrics

- `create_parameter_analysis_plots(results_df, filename='parameter_analysis_patients.png')`
  Creates line plots showing the effect of the number of patients on:
  - Average patient time
  - Idle time
  - Overtime

- `create_doctors_analysis_plots(results_df)`
  Creates line plots showing the effect of the number of consulting rooms on:
  - Average patient time
  - Idle time
  - Overtime

- `run_parameter_sweep_patients(num_runs, patients_range, num_registration_desks, num_doctors)`
  Analyses the effect of the number of patients on the metrics with a fixed number of consulting rooms. Tests various patient counts and runs `num_runs` simulations of both systems for each. Saves results to `analiza_wplyw_pacjentow.csv` and generates the corresponding plots.

- `run_parameter_sweep_doctors(num_runs, doctors_range, num_registration_desks, num_patients)`
  Analyses the effect of the number of consulting rooms on the metrics with a fixed number of patients. Tests various room counts and runs `num_runs` simulations of both systems for each. Saves results to `analiza_wplyw_gabinetow.csv` and generates the corresponding plots.

### Output files

The `analysis.py` module generates the following files in the `results/` directory:

**CSV:**

- `statystyki_opisowe.csv` – statistics for both systems (mean, median, std, percentiles)
- `testy_statystyczne_z.csv` – results of the Z-tests comparing both systems
- `dane_zagregowane.csv` – summary of results (means, standard deviations)
- `dane_surowe.csv` – all raw results from individual simulation runs
- `analiza_wplyw_pacjentow.csv` – effect of the number of patients on the metrics
- `analiza_wplyw_gabinetow.csv` – effect of the number of consulting rooms on the metrics

**Plots (PNG):**

- `comparison_avg_patient_time.png` – histograms of average patient time
- `comparison_overtime.png` – histograms of overtime
- `comparison_boxplots.png` – boxplots of both metrics
- `parameter_analysis_patients.png` – plots of the effect of the number of patients
- `parameter_analysis_doctors.png` – plots of the effect of the number of consulting rooms

## Usage

### Basic simulation

```bash
python src/main.py
```

Before running, you can change the parameters of the `run_scheduled_simulation` and `run_walk_in_simulation` calls in `main.py` to try other configurations of consulting rooms, registration desks or patients.

### Statistical analysis

```bash
python src/analysis.py
```

Runs the full analysis with the default parameters:

- 100 repetitions of each simulation
- 2 registration desks
- 5 consulting rooms (for the main analysis)
- 150 patients (for the main analysis)
- Patient-count sweep: (10, 20, 30, ..., 300)
- Consulting-room sweep: (1, 2, 3, ..., 10)

Parameters can be changed by editing the `run_full_analysis()` call in the `if __name__ == "__main__":` block.
