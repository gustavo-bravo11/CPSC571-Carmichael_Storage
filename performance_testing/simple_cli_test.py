#!/usr/bin/env python3
"""
Simple CLI Performance Test Runner for Carmichael Number Database

This script runs performance tests and displays results directly to the
command line interface in a simple, readable format. No CSV or visualization
files are generated.

Usage:
    python simple_cli_test.py [--runs N] [--testing-dir PATH]
"""

import argparse
import sys
from datetime import datetime
import time

from database_interface import SingleTableDB, MultiTableDB
from test_case_loader import TestCaseLoader
from test_runner import TestRunner


def print_header():
    """Print the test header."""
    print("\n" + "="*80)
    print("CARMICHAEL NUMBER DATABASE - SIMPLE PERFORMANCE TEST")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")


def print_test_case_header(test_num, total_tests, test_case):
    """Print header for each test case."""
    print(f"\n[Test {test_num}/{total_tests}]")
    print(f"  Factors: {test_case.factors}")
    print(f"  Factor Count: {len(test_case.factors)}")
    print(f"  Source: {test_case.test_file}:{test_case.line_number}")
    print("-" * 60)


def print_implementation_result(impl_name, stats):
    """Print results for a single implementation."""
    print(f"\n  {impl_name}:")
    print(f"    Mean Time:   {stats.mean_time*1000:>8.2f} ms")
    print(f"    Median Time: {stats.median_time*1000:>8.2f} ms")
    print(f"    Min Time:    {stats.min_time*1000:>8.2f} ms")
    print(f"    Max Time:    {stats.max_time*1000:>8.2f} ms")
    print(f"    Std Dev:     {stats.std_dev*1000:>8.2f} ms")
    print(f"    Found:       {'Yes' if stats.found else 'No'}")


def print_comparison(single_stats, multi_stats):
    """Print comparison between implementations."""
    if multi_stats.mean_time > 0:
        speedup = single_stats.mean_time / multi_stats.mean_time
        print(f"\n  Comparison:")
        print(f"    Speedup: {speedup:.2f}x", end="")

        if speedup > 1:
            print(f" (Multi-Table is {speedup:.2f}x faster)")
        elif speedup < 1:
            print(f" (Single Table is {1/speedup:.2f}x faster)")
        else:
            print(" (Same speed)")

        time_saved = (single_stats.mean_time - multi_stats.mean_time) * 1000
        print(f"    Time Difference: {abs(time_saved):.2f} ms")


def print_overall_summary(all_stats, single_impl_name, multi_impl_name):
    """Print overall summary of all tests."""
    print("\n\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)

    single_stats_list = all_stats[single_impl_name]
    multi_stats_list = all_stats[multi_impl_name]

    # Calculate totals
    single_total = sum(s.mean_time for s in single_stats_list) * 1000
    multi_total = sum(s.mean_time for s in multi_stats_list) * 1000

    # Calculate averages
    single_avg = single_total / len(single_stats_list) if single_stats_list else 0
    multi_avg = multi_total / len(multi_stats_list) if multi_stats_list else 0

    print(f"\nTotal Test Cases: {len(single_stats_list)}")

    print(f"\n{single_impl_name}:")
    print(f"  Total Time:   {single_total:>10.2f} ms")
    print(f"  Average Time: {single_avg:>10.2f} ms")

    print(f"\n{multi_impl_name}:")
    print(f"  Total Time:   {multi_total:>10.2f} ms")
    print(f"  Average Time: {multi_avg:>10.2f} ms")

    if multi_total > 0:
        overall_speedup = single_total / multi_total
        print(f"\nOverall Speedup: {overall_speedup:.2f}x")

        if overall_speedup > 1:
            print(f"{multi_impl_name} is {overall_speedup:.2f}x faster overall")
            print(f"Time saved: {(single_total - multi_total):.2f} ms total")
        elif overall_speedup < 1:
            print(f"{single_impl_name} is {1/overall_speedup:.2f}x faster overall")
            print(f"Time saved: {(multi_total - single_total):.2f} ms total")

    # Show distribution by factor count
    print("\n" + "-"*80)
    print("Performance by Factor Count:")
    print("-"*80)

    factor_count_map = {}
    for i, stats in enumerate(single_stats_list):
        num_factors = len(stats.test_case.factors)
        if num_factors not in factor_count_map:
            factor_count_map[num_factors] = []
        factor_count_map[num_factors].append(i)

    for num_factors in sorted(factor_count_map.keys()):
        indices = factor_count_map[num_factors]
        single_avg_for_count = sum(single_stats_list[i].mean_time for i in indices) / len(indices) * 1000
        multi_avg_for_count = sum(multi_stats_list[i].mean_time for i in indices) / len(indices) * 1000

        speedup = single_avg_for_count / multi_avg_for_count if multi_avg_for_count > 0 else 0

        print(f"  {num_factors} factors ({len(indices)} tests):")
        print(f"    Single Table avg: {single_avg_for_count:>8.2f} ms")
        print(f"    Multi-Table avg:  {multi_avg_for_count:>8.2f} ms")
        print(f"    Speedup:          {speedup:>8.2f}x")

    print("="*80)


def main():
    """Main entry point for simple CLI testing."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run simple CLI performance tests on Carmichael number database'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=5,
        help='Number of times to run each test (default: 5)'
    )
    parser.add_argument(
        '--testing-dir',
        type=str,
        default='testing',
        help='Directory containing test case files (default: testing)'
    )

    args = parser.parse_args()

    # Print header
    print_header()
    print(f"Configuration:")
    print(f"  Runs per test: {args.runs}")
    print(f"  Test directory: {args.testing_dir}")

    # Load test cases
    print(f"\nLoading test cases from '{args.testing_dir}'...")
    loader = TestCaseLoader(testing_dir=args.testing_dir)

    all_test_cases = []
    for filename, cases in loader.load_all_tests().items():
        all_test_cases.extend(cases)
        print(f"  Loaded {len(cases)} test(s) from {filename}")

    if not all_test_cases:
        print("\nError: No test cases found!")
        sys.exit(1)

    print(f"\nTotal test cases: {len(all_test_cases)}")

    # Initialize database implementations
    print("\nInitializing database connections...")
    try:
        single_table_db = SingleTableDB()
        multi_table_db = MultiTableDB()

        databases = [single_table_db, multi_table_db]

        print(f"  {single_table_db.get_implementation_name()}")
        print(f"  {multi_table_db.get_implementation_name()}")

    except Exception as e:
        print(f"\nError connecting to database: {e}")
        print("\nPlease ensure:")
        print("  1. PostgreSQL is running")
        print("  2. Database exists with the correct name")
        print("  3. .env file has correct database credentials")
        sys.exit(1)

    # Run tests
    print("\n" + "="*80)
    print("RUNNING TESTS")
    print("="*80)

    runner = TestRunner(num_runs=args.runs)
    all_stats = {db.get_implementation_name(): [] for db in databases}

    try:
        for test_num, test_case in enumerate(all_test_cases, 1):
            print_test_case_header(test_num, len(all_test_cases), test_case)

            # Run test for each implementation
            for db in databases:
                impl_name = db.get_implementation_name()

                # Run the test
                stats = runner.run_test_case(db, test_case, verbose=False)
                all_stats[impl_name].append(stats)

                # Print results
                print_implementation_result(impl_name, stats)

            # Print comparison
            single_impl_name = single_table_db.get_implementation_name()
            multi_impl_name = multi_table_db.get_implementation_name()

            print_comparison(
                all_stats[single_impl_name][-1],
                all_stats[multi_impl_name][-1]
            )

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Close database connections
        single_table_db.close()
        multi_table_db.close()

    # Print overall summary
    print_overall_summary(
        all_stats,
        single_table_db.get_implementation_name(),
        multi_table_db.get_implementation_name()
    )

    # Final message
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nTesting Complete!")


if __name__ == "__main__":
    main()
