import json
from dataclasses import dataclass

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LLM_REPORTS = {
    "gpt2": "gpt2",
    "llama3": "llama3",
    "nemo_llama3_input_guardrail": "llama3 + \nnemo input\nguardrail",
    "nemo_llama3_full_guardrail": "llama3 + \nnemo full\nguardrail",
    "guardrailsai_llama3": "llama3 + \nguardrails.ai",
}
"""Dict of tested LLMs from run_llm.py, where key is name of the LLM report and value is assigned label in chart."""


@dataclass
class ResultEntry:
    """An entry in the garak report .jsonl file with results."""

    entry_type: str
    probe: str
    detector: str
    passed: int
    total: int


@dataclass
class SingleResultValue:
    """A class to hold the results of a single probe."""

    passed: int = 0
    total: int = 0


def get_all_results_from_garak_reports() -> dict[str, dict[str, float]]:
    """Gather the results for all reports."""
    all_results = {}
    for llm_name, label in LLM_REPORTS.items():
        result = get_result_from_garak_report(f"runs/{llm_name}.report.jsonl")
        all_results[label] = result

    return all_results


def get_result_from_garak_report(path: str) -> dict[str, float]:
    """Generate the average results for each probe in the report file."""
    results: dict[str, SingleResultValue] = {}

    with open(path) as file:
        lines = file.readlines()

        for entry in lines:
            try:
                deserialized_entry = json.loads(entry)
                single_result = ResultEntry(**deserialized_entry)
            except TypeError:
                # Skip other entries that didn't match result dataclass.
                continue

            probe_name = single_result.probe.split(".")[0]

            results.setdefault(probe_name, SingleResultValue())
            results[probe_name].passed += single_result.passed
            results[probe_name].total += single_result.total

    avg_results = {probe_name: round(v.passed / v.total, 3) for probe_name, v in results.items()}

    return avg_results


def generate_plot_from_reports() -> None:
    """Plot heatmap of probes results for chosen reports."""
    df_reports = pd.DataFrame(get_all_results_from_garak_reports())

    colors = ["#B03A25", "#F0C179", "#3E8B05"]
    cmap = mcolors.LinearSegmentedColormap.from_list("", colors)

    # Generate the heatmap
    heatmap = sns.heatmap(
        df_reports,
        annot=True,
        fmt=".1%",
        cmap=cmap,
        cbar=False,
        linewidths=0.5,
        linecolor="white",
        annot_kws={"weight": "bold"},
    )
    heatmap.xaxis.tick_top()

    plt.tight_layout()
    plt.savefig("llm_garak_benchmark_result.svg")
    plt.show()


if __name__ == "__main__":
    generate_plot_from_reports()
