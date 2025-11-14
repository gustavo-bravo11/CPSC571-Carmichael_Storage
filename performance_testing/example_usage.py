"""
Example usage of the performance testing framework.

This script demonstrates how to use the framework programmatically
instead of through the command-line interface.
"""

from database_interface import SingleTableDB, MultiTableDB
from test_case_loader import TestCaseLoader, TestCase
from test_runner import TestRunner
from visualizer import PerformanceVisualizer


def example_1_basic_query():
    """Example 1: Simple query against both databases."""
    print("="*60)
    print("Example 1: Basic Query")
    print("="*60)

    # Test factors
    factors = [11, 13]
    print(f"Searching for Carmichael numbers with factors: {factors}")

    # Query single table
    with SingleTableDB() as single_db:
        result = single_db.query_by_factors(factors)
        if result:
            number, all_factors = result
            print(f"\n{single_db.get_implementation_name()} found:")
            print(f"  Number: {number}")
            print(f"  All factors: {all_factors}")

    # Query multi-table
    with MultiTableDB() as multi_db:
        result = multi_db.query_by_factors(factors)
        if result:
            number, all_factors = result
            print(f"\n{multi_db.get_implementation_name()} found:")
            print(f"  Number: {number}")
            print(f"  All factors: {all_factors}")


def example_2_manual_test_case():
    """Example 2: Run performance test on a single test case."""
    print("\n" + "="*60)
    print("Example 2: Manual Test Case Performance Measurement")
    print("="*60)

    # Create a test case manually
    test_case = TestCase(
        test_file="manual_test",
        line_number=1,
        product=143,
        factors=[11, 13]
    )

    print(f"Test case: {test_case.get_description()}")

    # Run test
    runner = TestRunner(num_runs=5)

    with SingleTableDB() as single_db:
        single_stats = runner.run_test_case(single_db, test_case, verbose=True)
        print(f"\n{single_stats}")

    with MultiTableDB() as multi_db:
        multi_stats = runner.run_test_case(multi_db, test_case, verbose=True)
        print(f"{multi_stats}")

    # Compare
    if multi_stats.mean_time > 0:
        speedup = single_stats.mean_time / multi_stats.mean_time
        print(f"\nSpeedup: {speedup:.2f}x")


def example_3_load_and_run_tests():
    """Example 3: Load test cases from files and run full suite."""
    print("\n" + "="*60)
    print("Example 3: Full Test Suite from Files")
    print("="*60)

    # Load test cases
    loader = TestCaseLoader(testing_dir="../testing")
    all_tests = loader.load_all_tests()

    # Take just first 3 test cases as example
    test_cases = []
    for filename, cases in all_tests.items():
        test_cases.extend(cases[:1])  # First case from each file
        if len(test_cases) >= 3:
            break

    print(f"Running {len(test_cases)} test cases...")

    # Initialize databases
    single_db = SingleTableDB()
    multi_db = MultiTableDB()
    databases = [single_db, multi_db]

    # Run tests
    runner = TestRunner(num_runs=3)
    stats = runner.run_all_tests(databases, test_cases, verbose=True)

    # Print summary
    runner.print_summary(stats)

    # Generate visualizations
    visualizer = PerformanceVisualizer(output_dir="example_results")
    visualizer.generate_all_visualizations(stats)

    # Cleanup
    single_db.close()
    multi_db.close()


def example_4_custom_implementation():
    """Example 4: How to create a custom database implementation."""
    print("\n" + "="*60)
    print("Example 4: Custom Database Implementation Template")
    print("="*60)

    print("""
To create a custom implementation, extend CarmichaelDatabase:

from database_interface import CarmichaelDatabase
from typing import List, Optional, Tuple
from decimal import Decimal

class MyCustomDB(CarmichaelDatabase):
    def get_implementation_name(self) -> str:
        return "My Custom Implementation"

    def get_table_info(self) -> str:
        return "Description of your table structure"

    def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]:
        # Your custom query logic here
        with self.connection.cursor() as cur:
            # Execute your custom query
            # Return (number, factors) tuple or None
            pass

Then use it like:

    with MyCustomDB() as custom_db:
        result = custom_db.query_by_factors([11, 13])
    """)


def example_5_analyzing_factor_count():
    """Example 5: Analyze how factor count affects performance."""
    print("\n" + "="*60)
    print("Example 5: Factor Count Analysis")
    print("="*60)

    # Create test cases with different factor counts
    test_cases = [
        TestCase("test", 1, 143, [11, 13]),           # 2 factors
        TestCase("test", 2, 561, [3, 11, 17]),        # 3 factors
        TestCase("test", 3, 1105, [5, 13, 17]),       # 3 factors
        TestCase("test", 4, 41041, [7, 11, 13, 41]),  # 4 factors
    ]

    runner = TestRunner(num_runs=3)

    with SingleTableDB() as single_db, MultiTableDB() as multi_db:
        print("\nTesting different factor counts...\n")

        for test_case in test_cases:
            print(f"Factors: {test_case.factors} (count: {len(test_case.factors)})")

            single_stats = runner.run_test_case(single_db, test_case, verbose=False)
            multi_stats = runner.run_test_case(multi_db, test_case, verbose=False)

            speedup = single_stats.mean_time / multi_stats.mean_time if multi_stats.mean_time > 0 else 0

            print(f"  Single Table: {single_stats.mean_time*1000:.2f}ms")
            print(f"  Multi-Table:  {multi_stats.mean_time*1000:.2f}ms")
            print(f"  Speedup:      {speedup:.2f}x")
            print()


if __name__ == "__main__":
    # Run examples
    # Uncomment the examples you want to run

    example_1_basic_query()
    # example_2_manual_test_case()
    # example_3_load_and_run_tests()
    # example_4_custom_implementation()
    # example_5_analyzing_factor_count()

    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
