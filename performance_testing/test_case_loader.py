"""
Test Case Loader for Carmichael Number Performance Testing

Loads test cases from the testing/ directory and parses them into
structured test cases for database queries.
"""

import os
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a single test case with factors to query."""
    test_file: str
    line_number: int
    product: int  # The product of factors (first number in line, ignored for queries)
    factors: List[int]  # The prime factors to search for

    def __str__(self):
        return f"{self.test_file}:L{self.line_number} (factors: {self.factors})"

    def get_description(self):
        """Get a human-readable description of this test case."""
        return f"{len(self.factors)} factors: {' × '.join(str(f) for f in self.factors)}"


class TestCaseLoader:
    """Loads and parses test cases from text files."""

    def __init__(self, testing_dir: str = "testing"):
        """
        Initialize test case loader.

        Args:
            testing_dir: Path to directory containing test files
        """
        self.testing_dir = testing_dir

    def load_test_file(self, filename: str) -> List[TestCase]:
        """
        Load test cases from a single file.

        Args:
            filename: Name of the test file

        Returns:
            List of TestCase objects parsed from the file
        """
        filepath = os.path.join(self.testing_dir, filename)
        test_cases = []

        # Skip 1_primes.txt as specified by user
        if filename == "1_primes.txt":
            return test_cases

        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    # Parse line: <product> <factor1> <factor2> ...
                    parts = line.split()
                    if len(parts) < 2:
                        continue

                    try:
                        product = int(parts[0])
                        factors = [int(f) for f in parts[1:]]

                        test_case = TestCase(
                            test_file=filename,
                            line_number=line_num,
                            product=product,
                            factors=factors
                        )
                        test_cases.append(test_case)
                    except ValueError:
                        # Skip lines that can't be parsed
                        continue

        except FileNotFoundError:
            print(f"Warning: Test file not found: {filepath}")

        return test_cases

    def load_all_tests(self) -> Dict[str, List[TestCase]]:
        """
        Load all test cases from the testing directory.

        Returns:
            Dictionary mapping filename to list of test cases
        """
        all_tests = {}

        if not os.path.exists(self.testing_dir):
            print(f"Warning: Testing directory not found: {self.testing_dir}")
            return all_tests

        # Get all .txt files in testing directory
        test_files = sorted([
            f for f in os.listdir(self.testing_dir)
            if f.endswith('.txt') and f != '1_primes.txt'
        ])

        for filename in test_files:
            test_cases = self.load_test_file(filename)
            if test_cases:
                all_tests[filename] = test_cases

        return all_tests

    def get_test_summary(self) -> str:
        """Get a summary of all loaded test cases."""
        all_tests = self.load_all_tests()
        total_cases = sum(len(cases) for cases in all_tests.values())

        summary = f"Loaded {total_cases} test cases from {len(all_tests)} files:\n"
        for filename, cases in all_tests.items():
            summary += f"  - {filename}: {len(cases)} cases\n"

        return summary
