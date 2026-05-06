# Delta Hedging Simulation

## Overview

This project studies delta hedging for a European call option in the Black-Scholes framework. The goal is to simulate stock price paths, hedge the sold option using delta, rebalance the hedge at discrete times, and measure the resulting hedging error.

## Project Tasks

1. Simulate stock price paths.
2. Sell an option and hedge using the delta of the option.
3. Rebalance the hedge periodically.
4. Track hedging error over time.

## Repository Structure

- `delta_hedging_jupyter.ipynb` contains the notebook version for GitHub and Google Colab.
- `main.py` runs the full simulation and generates plots and summaries.
- `src/gbm.py` contains the Geometric Brownian Motion stock-path simulation.
- `src/bs_model.py` contains the Black-Scholes call price and delta formulas.
- `src/hedging.py` contains the discrete delta hedging logic.
- `src/simulation.py` runs the Monte Carlo hedging experiment.
- `src/experiments.py` contains sensitivity experiments for frequency, volatility, and moneyness.
- `src/plots.py` creates the figures used in the report.
- `imgs/` stores the final plots.
- `results/` stores the numerical summaries.

## Methods

The stock price is modeled using Geometric Brownian Motion under the risk-neutral measure. For each simulated path, a European call option is sold and hedged using the Black-Scholes delta. The hedge is rebalanced at discrete time intervals, and the final hedging error is computed at maturity. Monte Carlo simulation is then used to study the distribution of these errors across many paths.

## Main Results

- The mean hedging error is close to zero.
- Hedging error variance increases when rebalancing becomes less frequent.
- Higher volatility produces larger hedging errors.
- Moneyness affects the stability of the hedge.
- Delta hedging reduces risk, but discrete hedging does not eliminate it completely.

## Figures

The repository includes the following final figures:

- `imgs/sample_gbm_paths.png`
- `imgs/single_path_diagnostics.png`
- `imgs/portfolio_value_paths.png`
- `imgs/average_hedging_error.png`
- `imgs/hedging_error_histogram.png`
- `imgs/frequency_vs_error.png`
- `imgs/volatility_vs_error.png`
- `imgs/moneyness_vs_error.png`

## Requirements

- Python 3
- NumPy
- Matplotlib

## Usage

To run the file-based version:

```bash
python main.py
```

To view the notebook version, open:

```bash
delta_hedging_jupyter.ipynb
```

## Notes

- The notebook and file-based version follow the same simulation logic.
- The GBM section in `src/gbm.py` is preserved as provided.
