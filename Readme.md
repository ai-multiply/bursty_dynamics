# Bursty dynamics

Bursty dynamics package is a python librarty designed to identify bursts of activity in longitudinal data/ (focus on EHR). It offers functionality to calculate burst parameters, memeory coefficient, and detect clusters of events in close temporal proximity to each other. 

credit: 
This package implements the alternate burst parameter described in the paper ‘Measuring Burstiness for Finite Event Sequences’ by Kim, Eun-Kyeong, and Hang-Hyun Jo, and memeory coefficient described in . ‘Burstiness and Memory in Complex Systems’ by Goh, K.-I., and A.-L. Barabási. 

other papers of influence:

visuals?


## Features

- Burst Parameter Calculation: Calculate burst parameters to quantify the intensity and frequency of bursts within longitudinal data. 
- Memory Coefficient Computation: Compute memory coefficients to assess the persistence of burst patterns over time.
- Train Detection: Identify clusters of events occurring in close temporal proximity.

## Installation

You can install the Burst identifier via pip:
```sh
pip install bursty_dynamics
```

## Usage
Here's a quick overview of how to use the main functionalities of the package:

```sh
import bursty_dynamics as bd

# Load your longitudinal data into a DataFrame
# df = load_data()

# Calculate burst parameters
burst_params = bd.calculate_scores(df, patient_id, time_col)
```


Notebook of usage. error handling. synthetic data - MIMIC, biobank?. 

## License


## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.




