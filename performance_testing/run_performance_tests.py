#!/usr/bin/env python3
"""
Main script for running Carmichael Number database performance tests.

This script compares the performance of two database implementations:
1. Single table approach: all Carmichael numbers in one table
2. Multi-table approach: partitioned by factor count (3-14 factors)

Usage:
    python run_performance_tests.py [--runs N] [--testing-dir PATH]
"""

import argparse
import sys
import csv
from datetime import datetime

from database_interface import SingleTableDB, MultiTableDB
from test_case_loader import TestCaseLoader
from test_runner import TestRunner
from visualizer import PerformanceVisualizer


def save_results_to_csv(comparison_data, filename="performance_results.csv"):
    """
    Save detailed results to CSV file.

    Args:
        comparison_data: List of dictionaries with test results
        filename: Output CSV filename
    """
    if not comparison_data:
        print("No data to save")
        return

    filepath = f"performance_results/{filename}"

    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = comparison_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in comparison_data:
            writer.writerow(row)

    print(f"Saved detailed results to {filepath}")


def main():
    """Main entry point for performance testing."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run performance tests on Carmichael number database implementations'
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
    parser.add_argument(
        '--output-dir',
        type=str,
        default='performance_results',
        help='Directory for output files (default: performance_results)'
    )
    parser.add_argument(
        '--no-viz',
        action='store_true',
        help='Skip generating visualizations'
    )

    args = parser.parse_args()

    # Print header
    print("="*80)
    print("CARMICHAEL NUMBER DATABASE PERFORMANCE TESTING")
    print("="*80)
    print(f"Test runs per query: {args.runs}")
    print(f"Test directory: {args.testing_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)

    # Load test cases
    print("\n[1/5] Loading test cases...")
    loader = TestCaseLoader(testing_dir=args.testing_dir)
    print(loader.get_test_summary())

    all_test_cases = []
    for filename, cases in loader.load_all_tests().items():
        all_test_cases.extend(cases)

    if not all_test_cases:
        print("Error: No test cases found!")
        sys.exit(1)

    print(f"Total test cases to run: {len(all_test_cases)}")

    # Initialize database implementations
    print("\n[2/5] Initializing database connections...")
    try:
        single_table_db = SingleTableDB()
        multi_table_db = MultiTableDB()

        databases = [single_table_db, multi_table_db]

        print(f"  - {single_table_db.get_implementation_name()}: {single_table_db.get_table_info()}")
        print(f"  - {multi_table_db.get_implementation_name()}: {multi_table_db.get_table_info()}")

    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nPlease ensure:")
        print("  1. PostgreSQL is running")
        print("  2. Database 'cm_numbers' exists")
        print("  3. .env file has correct database credentials")
        sys.exit(1)

    # Run tests
    print("\n[3/5] Running performance tests...")
    print(f"This will execute {len(all_test_cases) * len(databases) * args.runs} queries total")

    runner = TestRunner(num_runs=args.runs)

    try:
        stats = runner.run_all_tests(
            databases=databases,
            test_cases=all_test_cases,
            verbose=True
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

    # Print summary
    print("\n[4/5] Generating summary...")
    runner.print_summary(stats)

    # Save detailed results to CSV
    comparison_data = runner.get_comparison_table(stats)
    save_results_to_csv(
        comparison_data,
        filename=f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    # Generate visualizations
    if not args.no_viz:
        print("\n[5/5] Generating visualizations...")
        visualizer = PerformanceVisualizer(output_dir=args.output_dir)

        try:
            visualizer.generate_all_visualizations(stats)
        except Exception as e:
            print(f"Warning: Failed to generate some visualizations: {e}")
            print("You may need to install matplotlib: pip install matplotlib")
    else:
        print("\n[5/5] Skipping visualizations (--no-viz flag set)")

    # Final summary
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Results saved to: {args.output_dir}/")
    print("="*80)


if __name__ == "__main__":
    main()
