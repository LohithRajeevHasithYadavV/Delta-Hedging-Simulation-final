from __future__ import annotations

import numpy as np

from .simulation import run_simulation


def compute_stats(errors: np.ndarray) -> dict:
    return {
        "mean": float(np.mean(errors)),
        "std": float(np.std(errors, ddof=1)),
        "rmse": float(np.sqrt(np.mean(errors ** 2))),
        "mean_abs_error": float(np.mean(np.abs(errors))),
    }


def experiment_hedge_frequency(S0: float, K: float, T: float, r: float, sigma: float, M: int, seed: int = 42) -> dict:
    frequencies = {
        "Daily": 252,
        "Weekly": 52,
        "Monthly": 12
    }

    results = {}

    for label, N in frequencies.items():
        _, hedge_data = run_simulation(S0, K, T, r, sigma, N, M, seed=seed)
        results[label] = compute_stats(hedge_data["errors"])

    return results


def experiment_volatility(S0: float, K: float, T: float, r: float, N: int, M: int, seed: int = 42) -> dict:
    sigmas = {
        "Low Volatility": 0.15,
        "High Volatility": 0.35
    }

    results = {}

    for label, sigma in sigmas.items():
        _, hedge_data = run_simulation(S0, K, T, r, sigma, N, M, seed=seed)
        results[label] = compute_stats(hedge_data["errors"])

    return results


def experiment_moneyness(S0: float, T: float, r: float, sigma: float, N: int, M: int, seed: int = 42) -> dict:
    strikes = {
        "ITM": 0.9 * S0,
        "ATM": 1.0 * S0,
        "OTM": 1.1 * S0
    }

    results = {}

    for label, K in strikes.items():
        _, hedge_data = run_simulation(S0, K, T, r, sigma, N, M, seed=seed)
        results[label] = compute_stats(hedge_data["errors"])

    return results
