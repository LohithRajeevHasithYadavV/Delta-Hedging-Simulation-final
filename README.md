# Delta Hedging Simulation for European Options

## Overview

This project studies delta hedging for a European call option under the Black-Scholes framework. The objective is to simulate stock price paths, hedge the sold option using delta, rebalance the hedge at discrete time intervals, and analyze the resulting hedging error.

The project follows four main tasks:

1. Simulate stock price paths.
2. Sell an option and hedge using the delta of the option.
3. Rebalance the hedge periodically.
4. Track hedging error over time.

## Main Notebook

The complete project is presented in the notebook:

- `delta_hedging_jupyter.ipynb`

This notebook contains the simulation flow, numerical summaries, and the final plots used in the report.

## Model Summary

The stock price is modeled using Geometric Brownian Motion under the risk-neutral measure. The option is priced using the Black-Scholes formula, and the hedge ratio is computed from the option delta. Since the hedge is rebalanced only at discrete times, the strategy is not perfect and produces a nonzero hedging error.

## Key Results

The simulation demonstrates the following:

- Delta hedging reduces risk but does not eliminate it completely.
- Discrete rebalancing introduces tracking error.
- Higher rebalancing frequency reduces the spread of hedging error.
- Higher volatility increases hedging error.
- Option moneyness affects hedge stability.

## Figures

### Simulated GBM Paths

![Sample GBM Paths](imgs/sample_gbm_paths.png)

### Single Path Delta Hedging Diagnostics

![Single Path Diagnostics](imgs/single_path_diagnostics.png)

### Portfolio Value Through Time

![Portfolio Value Paths](imgs/portfolio_value_paths.png)

### Average Hedging Error Through Time

![Average Hedging Error](imgs/average_hedging_error.png)

### Distribution of Hedging Error

![Hedging Error Histogram](imgs/hedging_error_histogram.png)

### Rebalancing Frequency and Hedging Error

![Frequency vs Error](imgs/frequency_vs_error.png)

### Volatility and Hedging Error

![Volatility vs Error](imgs/volatility_vs_error.png)

### Moneyness and Hedging Error

![Moneyness vs Error](imgs/moneyness_vs_error.png)

## Repository Structure

- `delta_hedging_jupyter.ipynb` : main notebook version of the project
- `main.py` : file-based driver script
- `src/gbm.py` : stock path simulation using Geometric Brownian Motion
- `src/bs_model.py` : Black-Scholes pricing and delta functions
- `src/hedging.py` : discrete delta hedging implementation
- `src/simulation.py` : Monte Carlo simulation wrapper
- `src/experiments.py` : sensitivity analysis for frequency, volatility, and moneyness
- `src/plots.py` : plot generation
- `imgs/` : final figures

## Requirements

- Python 3
- NumPy
- Matplotlib
- Jupyter Notebook or Google Colab

## How to Run

To use the notebook version, open:

`delta_hedging_jupyter.ipynb`

To run the file-based version:

```bash
python main.py


## Notes

- The notebook and file-based version follow the same simulation logic.
