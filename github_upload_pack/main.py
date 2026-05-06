from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "delta-hedging-mpl"))

from src.bs_model import validate_black_scholes
from src.experiments import experiment_hedge_frequency, experiment_moneyness, experiment_volatility
from src.gbm import GBMConfig, simulate_gbm_paths, validate_gbm_paths, plot_sample_paths
from src.hedging import delta_hedge_single_path, run_delta_hedge
from src.plots import (
    plot_average_hedging_error,
    plot_error_histogram,
    plot_frequency_vs_error,
    plot_moneyness_vs_error,
    plot_portfolio_paths,
    plot_single_path,
    plot_volatility_vs_error,
)


def ensure_output_dirs() -> None:
    Path("imgs").mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(parents=True, exist_ok=True)


def save_summary(summary: dict, output_path: str, title: str) -> None:
    lines = [title]
    for key, value in summary.items():
        if isinstance(value, float):
            lines.append(f"{key}: {value:.6f}")
        else:
            lines.append(f"{key}: {value}")
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_experiment_results(results: dict, output_path: str, title: str) -> None:
    lines = [title]
    for label, stats in results.items():
        lines.append("")
        lines.append(label)
        for key, value in stats.items():
            lines.append(f"{key}: {value:.6f}")
    Path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(
    gbm_summary: dict,
    bs_summary: dict,
    hedge_summary: dict,
    frequency_results: dict,
    volatility_results: dict,
    moneyness_results: dict,
) -> None:
    report_lines = [
        "# Delta Hedging Simulation",
        "",
        "## Project Statement",
        "Delta hedging attempts to neutralize price sensitivity by adjusting the stock position against an option position.",
        "",
        "This project studies four tasks:",
        "1. Simulate stock price paths.",
        "2. Sell a call option and hedge with the option delta.",
        "3. Rebalance the hedge periodically.",
        "4. Track hedging error over time.",
        "",
        "## Model Setup",
        "- Stock paths follow geometric Brownian motion.",
        "- Option prices and deltas are computed using the Black-Scholes formula.",
        "- The hedge is rebalanced at discrete times.",
        "",
        "## GBM Validation",
    ]

    for key, value in gbm_summary.items():
        report_lines.append(f"- {key}: {value:.6f}")

    report_lines.extend(["", "## Black-Scholes Checks"])
    for key, value in bs_summary.items():
        if isinstance(value, float):
            report_lines.append(f"- {key}: {value:.6f}")
        else:
            report_lines.append(f"- {key}: {value}")

    report_lines.extend(["", "## Hedging Results"])
    for key, value in hedge_summary.items():
        report_lines.append(f"- {key}: {value:.6f}")

    report_lines.extend(["", "## Rebalancing Frequency"])
    for label, stats in frequency_results.items():
        report_lines.append(
            f"- {label}: std={stats['std']:.6f}, rmse={stats['rmse']:.6f}, mean abs error={stats['mean_abs_error']:.6f}"
        )

    report_lines.extend(["", "## Volatility"])
    for label, stats in volatility_results.items():
        report_lines.append(
            f"- {label}: std={stats['std']:.6f}, rmse={stats['rmse']:.6f}, mean abs error={stats['mean_abs_error']:.6f}"
        )

    report_lines.extend(["", "## Moneyness"])
    for label, stats in moneyness_results.items():
        report_lines.append(
            f"- {label}: std={stats['std']:.6f}, rmse={stats['rmse']:.6f}, mean abs error={stats['mean_abs_error']:.6f}"
        )

    report_lines.extend(
        [
            "",
            "## Discussion",
            "- More frequent rebalancing lowers the spread of the hedging error.",
            "- Higher volatility increases the hedging error because the portfolio must react to larger price moves.",
            "- Moneyness changes the delta profile and therefore changes hedge quality.",
        ]
    )

    Path("results/project_report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")


def print_summary(title: str, summary: dict) -> None:
    print(title)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.6f}")
        else:
            print(f"{key}: {value}")
    print()


def print_experiment_results(title: str, results: dict) -> None:
    print(title)
    for label, stats in results.items():
        print(label)
        for key, value in stats.items():
            print(f"{key}: {value:.6f}")
        print()


def main() -> None:
    ensure_output_dirs()

    cfg = GBMConfig(
        S0=100.0,
        r=0.05,
        sigma=0.2,
        T=1.0,
        N=252,
        M=10000,
        seed=42,
    )
    K = 100.0

    paths = simulate_gbm_paths(cfg.S0, cfg.r, cfg.sigma, cfg.T, cfg.N, cfg.M, cfg.seed)
    gbm_summary = validate_gbm_paths(paths, cfg.S0, cfg.r, cfg.sigma, cfg.T)
    bs_summary = validate_black_scholes(K, cfg.T, cfg.r, cfg.sigma)
    hedge_data = run_delta_hedge(paths, K, cfg.T, cfg.r, cfg.sigma)
    single_path_data = delta_hedge_single_path(paths[0], K, cfg.T, cfg.r, cfg.sigma, cfg.T / cfg.N)

    frequency_results = experiment_hedge_frequency(cfg.S0, K, cfg.T, cfg.r, cfg.sigma, cfg.M, seed=cfg.seed)
    volatility_results = experiment_volatility(cfg.S0, K, cfg.T, cfg.r, cfg.N, cfg.M, seed=cfg.seed)
    moneyness_results = experiment_moneyness(cfg.S0, cfg.T, cfg.r, cfg.sigma, cfg.N, cfg.M, seed=cfg.seed)

    save_summary(gbm_summary, "results/gbm_summary.txt", "GBM Validation")
    save_summary(bs_summary, "results/black_scholes_summary.txt", "Black-Scholes Checks")
    save_summary(hedge_data["summary"], "results/hedging_summary.txt", "Delta Hedging Summary")
    save_experiment_results(frequency_results, "results/frequency_experiment.txt", "Rebalancing Frequency")
    save_experiment_results(volatility_results, "results/volatility_experiment.txt", "Volatility Scenarios")
    save_experiment_results(moneyness_results, "results/moneyness_experiment.txt", "Moneyness Scenarios")

    plot_sample_paths(paths, cfg.T, num_paths=50, title="Simulated GBM Price Paths")
    plot_single_path(paths[0], single_path_data, cfg.T, "imgs/single_path_diagnostics.png")
    plot_error_histogram(hedge_data["errors"], "imgs/hedging_error_histogram.png")
    plot_portfolio_paths(hedge_data["time_grid"], hedge_data["portfolio_values"], "imgs/portfolio_value_paths.png")
    plot_average_hedging_error(hedge_data["time_grid"], hedge_data["portfolio_values"], "imgs/average_hedging_error.png")
    plot_frequency_vs_error(frequency_results, "imgs/frequency_vs_error.png")
    plot_volatility_vs_error(volatility_results, "imgs/volatility_vs_error.png")
    plot_moneyness_vs_error(moneyness_results, "imgs/moneyness_vs_error.png")

    write_report(
        gbm_summary,
        bs_summary,
        hedge_data["summary"],
        frequency_results,
        volatility_results,
        moneyness_results,
    )

    print_summary("GBM validation", gbm_summary)
    print_summary("Black-Scholes checks", bs_summary)
    print_summary("Delta hedging summary", hedge_data["summary"])
    print_experiment_results("Rebalancing frequency", frequency_results)
    print_experiment_results("Volatility scenarios", volatility_results)
    print_experiment_results("Moneyness scenarios", moneyness_results)


if __name__ == "__main__":
    main()
