"""
Visualization Module for Carmichael Number Performance Testing

Creates charts and graphs to compare performance between database implementations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, List
import numpy as np
from test_runner import TestRunStats
import os


class PerformanceVisualizer:
    """Creates visualizations of performance test results."""

    def __init__(self, output_dir: str = "performance_results"):
        """
        Initialize visualizer.

        Args:
            output_dir: Directory to save visualization files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_comparison_bar_chart(
        self,
        stats: Dict[str, List[TestRunStats]],
        filename: str = "comparison_bar_chart.png"
    ):
        """
        Create a bar chart comparing execution times.

        Args:
            stats: Dictionary mapping implementation name to test statistics
            filename: Output filename for the chart
        """
        implementations = list(stats.keys())
        num_tests = len(stats[implementations[0]])

        # Prepare data
        test_labels = []
        impl_means = {impl: [] for impl in implementations}

        for i in range(num_tests):
            test_case = stats[implementations[0]][i].test_case
            label = f"{test_case.test_file}\nL{test_case.line_number}"
            test_labels.append(label)

            for impl in implementations:
                impl_means[impl].append(stats[impl][i].mean_time * 1000)  # Convert to ms

        # Create plot
        x = np.arange(len(test_labels))
        width = 0.35
        fig, ax = plt.subplots(figsize=(14, 8))

        # Create bars for each implementation
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        for idx, (impl, means) in enumerate(impl_means.items()):
            offset = width * (idx - len(implementations)/2 + 0.5)
            ax.bar(x + offset, means, width, label=impl, color=colors[idx % len(colors)])

        # Customize plot
        ax.set_xlabel('Test Case', fontsize=12, fontweight='bold')
        ax.set_ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Query Execution Time Comparison by Test Case', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(test_labels, rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Saved bar chart to {os.path.join(self.output_dir, filename)}")

    def plot_speedup_chart(
        self,
        stats: Dict[str, List[TestRunStats]],
        baseline: str = "Single Table",
        filename: str = "speedup_chart.png"
    ):
        """
        Create a chart showing speedup of other implementations vs baseline.

        Args:
            stats: Dictionary mapping implementation name to test statistics
            baseline: Name of baseline implementation for comparison
            filename: Output filename for the chart
        """
        if baseline not in stats:
            print(f"Warning: Baseline '{baseline}' not found in stats")
            return

        implementations = [impl for impl in stats.keys() if impl != baseline]
        num_tests = len(stats[baseline])

        # Prepare data
        test_labels = []
        speedups = {impl: [] for impl in implementations}

        for i in range(num_tests):
            test_case = stats[baseline][i].test_case
            label = f"{test_case.test_file}\nL{test_case.line_number}"
            test_labels.append(label)

            baseline_time = stats[baseline][i].mean_time

            for impl in implementations:
                impl_time = stats[impl][i].mean_time
                if impl_time > 0:
                    speedup = baseline_time / impl_time
                else:
                    speedup = 0
                speedups[impl].append(speedup)

        # Create plot
        fig, ax = plt.subplots(figsize=(14, 8))
        x = np.arange(len(test_labels))
        width = 0.7

        # Plot speedup bars
        for idx, (impl, speedup_values) in enumerate(speedups.items()):
            colors = ['#2ecc71' if s > 1 else '#e74c3c' for s in speedup_values]
            ax.bar(x, speedup_values, width, label=impl, color=colors, alpha=0.7)

        # Add horizontal line at y=1 (no speedup)
        ax.axhline(y=1, color='black', linestyle='--', linewidth=1, label='No speedup')

        # Customize plot
        ax.set_xlabel('Test Case', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'Speedup vs {baseline}', fontsize=12, fontweight='bold')
        ax.set_title(f'Performance Speedup Relative to {baseline}', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(test_labels, rotation=45, ha='right', fontsize=9)
        ax.grid(axis='y', alpha=0.3)

        # Add legend
        green_patch = mpatches.Patch(color='#2ecc71', label='Faster than baseline', alpha=0.7)
        red_patch = mpatches.Patch(color='#e74c3c', label='Slower than baseline', alpha=0.7)
        ax.legend(handles=[green_patch, red_patch])

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Saved speedup chart to {os.path.join(self.output_dir, filename)}")

    def plot_factor_count_analysis(
        self,
        stats: Dict[str, List[TestRunStats]],
        filename: str = "factor_count_analysis.png"
    ):
        """
        Analyze performance by number of factors.

        Args:
            stats: Dictionary mapping implementation name to test statistics
            filename: Output filename for the chart
        """
        implementations = list(stats.keys())

        # Group by factor count
        factor_counts = {}
        for impl in implementations:
            factor_counts[impl] = {}
            for test_stats in stats[impl]:
                num_factors = len(test_stats.test_case.factors)
                if num_factors not in factor_counts[impl]:
                    factor_counts[impl][num_factors] = []
                factor_counts[impl][num_factors].append(test_stats.mean_time * 1000)

        # Calculate averages
        factor_count_avg = {}
        all_factor_nums = set()
        for impl in implementations:
            factor_count_avg[impl] = {}
            for num_factors, times in factor_counts[impl].items():
                factor_count_avg[impl][num_factors] = np.mean(times)
                all_factor_nums.add(num_factors)

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

        for idx, impl in enumerate(implementations):
            sorted_factors = sorted(factor_count_avg[impl].keys())
            avg_times = [factor_count_avg[impl][f] for f in sorted_factors]
            ax.plot(sorted_factors, avg_times, marker='o', linewidth=2,
                   markersize=8, label=impl, color=colors[idx % len(colors)])

        # Customize plot
        ax.set_xlabel('Number of Factors', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Execution Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Query Performance by Number of Factors', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xticks(sorted(all_factor_nums))

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Saved factor count analysis to {os.path.join(self.output_dir, filename)}")

    def plot_box_plot(
        self,
        stats: Dict[str, List[TestRunStats]],
        filename: str = "distribution_box_plot.png"
    ):
        """
        Create box plots showing distribution of execution times.

        Args:
            stats: Dictionary mapping implementation name to test statistics
            filename: Output filename for the chart
        """
        implementations = list(stats.keys())

        # Collect all run times for each implementation
        all_times = {impl: [] for impl in implementations}
        for impl in implementations:
            for test_stats in stats[impl]:
                all_times[impl].extend([t * 1000 for t in test_stats.run_times])

        # Create plot
        fig, ax = plt.subplots(figsize=(10, 7))

        positions = np.arange(len(implementations))
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

        bp = ax.boxplot(
            [all_times[impl] for impl in implementations],
            positions=positions,
            widths=0.6,
            patch_artist=True,
            labels=implementations
        )

        # Color the boxes
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Customize plot
        ax.set_ylabel('Execution Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Distribution of Query Execution Times', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close()

        print(f"Saved box plot to {os.path.join(self.output_dir, filename)}")

    def generate_all_visualizations(self, stats: Dict[str, List[TestRunStats]]):
        """
        Generate all available visualizations.

        Args:
            stats: Dictionary mapping implementation name to test statistics
        """
        print("\nGenerating visualizations...")

        self.plot_comparison_bar_chart(stats)
        self.plot_speedup_chart(stats)
        self.plot_factor_count_analysis(stats)
        self.plot_box_plot(stats)

        print(f"\nAll visualizations saved to '{self.output_dir}/' directory")
