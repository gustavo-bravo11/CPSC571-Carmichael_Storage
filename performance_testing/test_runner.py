"""
Test Runner for Carmichael Number Performance Testing

Executes test cases against different database implementations and
measures query execution time.
"""

import time
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
import statistics

from database_interface import CarmichaelDatabase
from test_case_loader import TestCase


@dataclass
class QueryResult:
    """Result of a single query execution."""
    test_case: TestCase
    implementation: str
    execution_time: float  # in seconds
    found: bool
    run_number: int


@dataclass
class TestRunStats:
    """Statistical summary of multiple runs of the same test."""
    test_case: TestCase
    implementation: str
    run_times: List[float] = field(default_factory=list)
    found: bool = False

    @property
    def mean_time(self) -> float:
        """Average execution time."""
        return statistics.mean(self.run_times) if self.run_times else 0.0

    @property
    def median_time(self) -> float:
        """Median execution time."""
        return statistics.median(self.run_times) if self.run_times else 0.0

    @property
    def min_time(self) -> float:
        """Minimum execution time."""
        return min(self.run_times) if self.run_times else 0.0

    @property
    def max_time(self) -> float:
        """Maximum execution time."""
        return max(self.run_times) if self.run_times else 0.0

    @property
    def std_dev(self) -> float:
        """Standard deviation of execution times."""
        return statistics.stdev(self.run_times) if len(self.run_times) > 1 else 0.0

    def __str__(self):
        return (f"{self.implementation}: "
                f"mean={self.mean_time*1000:.2f}ms, "
                f"median={self.median_time*1000:.2f}ms, "
                f"min={self.min_time*1000:.2f}ms, "
                f"max={self.max_time*1000:.2f}ms, "
                f"std={self.std_dev*1000:.2f}ms")


class TestRunner:
    """Executes performance tests against database implementations."""

    def __init__(self, num_runs: int = 5):
        """
        Initialize test runner.

        Args:
            num_runs: Number of times to run each test for statistical reliability
        """
        self.num_runs = num_runs
        self.results: List[QueryResult] = []

    def run_single_query(
        self,
        db: CarmichaelDatabase,
        test_case: TestCase,
        run_number: int
    ) -> QueryResult:
        """
        Execute a single query and measure execution time.

        Args:
            db: Database implementation to test
            test_case: Test case to execute
            run_number: Which run this is (for tracking)

        Returns:
            QueryResult with timing information
        """
        start_time = time.perf_counter()
        result = db.query_by_factors(test_case.factors)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        found = result is not None

        return QueryResult(
            test_case=test_case,
            implementation=db.get_implementation_name(),
            execution_time=execution_time,
            found=found,
            run_number=run_number
        )

    def run_test_case(
        self,
        db: CarmichaelDatabase,
        test_case: TestCase,
        verbose: bool = False
    ) -> TestRunStats:
        """
        Run a test case multiple times and collect statistics.

        Args:
            db: Database implementation to test
            test_case: Test case to execute
            verbose: Whether to print progress

        Returns:
            TestRunStats with aggregated results
        """
        stats = TestRunStats(
            test_case=test_case,
            implementation=db.get_implementation_name()
        )

        for run in range(1, self.num_runs + 1):
            if verbose:
                print(f"  Run {run}/{self.num_runs}...", end='\r')

            result = self.run_single_query(db, test_case, run)
            stats.run_times.append(result.execution_time)
            stats.found = result.found
            self.results.append(result)

        if verbose:
            print(f"  Completed {self.num_runs} runs" + " " * 20)

        return stats

    def run_all_tests(
        self,
        databases: List[CarmichaelDatabase],
        test_cases: List[TestCase],
        verbose: bool = True
    ) -> Dict[str, List[TestRunStats]]:
        """
        Run all test cases against all database implementations.

        Args:
            databases: List of database implementations to test
            test_cases: List of test cases to execute
            verbose: Whether to print progress

        Returns:
            Dictionary mapping implementation name to list of TestRunStats
        """
        all_stats = {db.get_implementation_name(): [] for db in databases}

        total_tests = len(test_cases) * len(databases)
        current_test = 0

        for test_case in test_cases:
            if verbose:
                print(f"\nTest: {test_case}")

            for db in databases:
                current_test += 1
                if verbose:
                    print(f"[{current_test}/{total_tests}] Testing with {db.get_implementation_name()}...")

                stats = self.run_test_case(db, test_case, verbose=verbose)
                all_stats[db.get_implementation_name()].append(stats)

                if verbose:
                    print(f"  {stats}")

        return all_stats

    def get_comparison_table(
        self,
        stats: Dict[str, List[TestRunStats]]
    ) -> List[Dict]:
        """
        Generate a comparison table of results.

        Args:
            stats: Dictionary of test run statistics

        Returns:
            List of dictionaries suitable for DataFrame or CSV export
        """
        comparison = []

        # Group stats by test case
        implementations = list(stats.keys())
        num_tests = len(stats[implementations[0]])

        for i in range(num_tests):
            row = {}
            test_case = stats[implementations[0]][i].test_case

            row['test_file'] = test_case.test_file
            row['line'] = test_case.line_number
            row['num_factors'] = len(test_case.factors)
            row['factors'] = str(test_case.factors)

            for impl in implementations:
                test_stats = stats[impl][i]
                row[f'{impl}_mean_ms'] = test_stats.mean_time * 1000
                row[f'{impl}_median_ms'] = test_stats.median_time * 1000
                row[f'{impl}_min_ms'] = test_stats.min_time * 1000
                row[f'{impl}_max_ms'] = test_stats.max_time * 1000
                row[f'{impl}_std_ms'] = test_stats.std_dev * 1000
                row[f'{impl}_found'] = test_stats.found

            # Calculate speedup (single table as baseline)
            if 'Single Table' in implementations and 'Multi-Table (Partitioned)' in implementations:
                single_mean = stats['Single Table'][i].mean_time
                multi_mean = stats['Multi-Table (Partitioned)'][i].mean_time

                if multi_mean > 0:
                    row['speedup'] = single_mean / multi_mean
                else:
                    row['speedup'] = float('inf')

            comparison.append(row)

        return comparison

    def print_summary(self, stats: Dict[str, List[TestRunStats]]):
        """Print a summary of test results."""
        print("\n" + "="*80)
        print("PERFORMANCE TEST SUMMARY")
        print("="*80)

        for impl_name, impl_stats in stats.items():
            total_time = sum(s.mean_time for s in impl_stats)
            avg_time = total_time / len(impl_stats) if impl_stats else 0

            print(f"\n{impl_name}:")
            print(f"  Total tests: {len(impl_stats)}")
            print(f"  Total time (mean): {total_time*1000:.2f}ms")
            print(f"  Average time per query: {avg_time*1000:.2f}ms")

        # Calculate overall comparison
        if len(stats) == 2:
            impl_names = list(stats.keys())
            total1 = sum(s.mean_time for s in stats[impl_names[0]])
            total2 = sum(s.mean_time for s in stats[impl_names[1]])

            if total2 > 0:
                speedup = total1 / total2
                print(f"\nOverall Speedup: {speedup:.2f}x")
                if speedup > 1:
                    print(f"{impl_names[1]} is {speedup:.2f}x faster")
                else:
                    print(f"{impl_names[0]} is {1/speedup:.2f}x faster")

        print("="*80)
