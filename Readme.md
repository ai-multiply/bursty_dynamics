# Bursty dynamics

Bursty dynamics is a package designed to identify bursts of activity in longitudinal data/ (focus on EHR). It offers functionality to calculate burstiness parameters, memeory coefficient, detect trains of events in close temporal proximity to each other, and also calculate the burstiness parameter and memory coefficient of the trains. 

credit: 
This package implements the alternate burst parameter described in the paper ‘Measuring Burstiness for Finite Event Sequences’ by Kim, Eun-Kyeong, and Hang-Hyun Jo, and memeory coefficient described in ‘Burstiness and Memory in Complex Systems’ by Goh, K.-I., and A.-L. Barabási. 

credit for train??


other papers of influence:



## Features

- Burst Parameter Calculation: Calculate burst parameters to quantify the intensity and frequency of bursts within longitudinal data. 
- Memory Coefficient Computation: Compute memory coefficients to assess the persistence of burst patterns over time.
- Train Detection: Identify clusters of events occurring in close temporal proximity.
- Train information

## Installation

You can install the bursty_dynamic via pip:
```sh
pip install bursty_dynamics
```

## Usage
Here's a quick overview of how to use the main functionalities of the package:

```sh
from bursty_dynamics.scores import calculate_scores
from bursty_dynamics.trains import train_detection, calculate_train_info, calculate_scores_train

# Load your longitudinal data into a DataFrame
# df = load_data()

# Calculate burst parameters
burst_params = calculate_scores(df, subject_id = 'eid', time_col = 'event_dt')
```

For more example of usage, please take a look at examples.ipynb in the example folder.

## License

`bursty_dynamics` was created by AI-Multiply in Queen Mary University of London. 

## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.




