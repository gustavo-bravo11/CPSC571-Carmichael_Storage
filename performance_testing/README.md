# Carmichael Number Database Performance Testing Framework

A modular testing framework to compare the performance of two database implementations for storing and querying Carmichael numbers.

## Overview

This framework compares two approaches to storing Carmichael numbers:

1. **Single Table**: All Carmichael numbers stored in one table (`carmichael_number`)
2. **Multi-Table (Partitioned)**: Numbers partitioned into 12 tables (`carmichael_number_3` through `carmichael_number_14`) based on factor count

The key hypothesis: When querying for numbers with many factors, the multi-table approach can skip tables with fewer factors, potentially improving query performance.

## Architecture

The framework is built with modularity in mind:

```
performance_testing/
├── database_interface.py     # Abstract interface + implementations
├── test_case_loader.py       # Loads test cases from files
├── test_runner.py            # Executes tests and measures performance
├── visualizer.py             # Generates performance charts
├── run_performance_tests.py  # Main entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

### Key Components

#### 1. Database Interface (`database_interface.py`)

Provides an abstract `CarmichaelDatabase` class with two concrete implementations:

- `SingleTableDB`: Queries the single `carmichael_number` table
- `MultiTableDB`: Intelligently queries only relevant partitioned tables

**Key Interface Method:**
```python
def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]
```

This method searches for Carmichael numbers containing all specified factors.

#### 2. Test Case Loader (`test_case_loader.py`)

Loads test cases from the `testing/` directory. Each test file contains lines in the format:
```
<product> <factor1> <factor2> ... <factorN>
```

The loader parses these into `TestCase` objects for querying.

#### 3. Test Runner (`test_runner.py`)

Executes each test case multiple times against each database implementation:

- Measures query execution time using `time.perf_counter()`
- Runs each test N times (default: 5) for statistical reliability
- Calculates mean, median, min, max, and standard deviation
- Provides speedup comparison between implementations

#### 4. Visualizer (`visualizer.py`)

Generates four types of visualizations:

1. **Comparison Bar Chart**: Side-by-side execution times for each test
2. **Speedup Chart**: Shows which implementation is faster per test
3. **Factor Count Analysis**: Performance trends based on number of factors
4. **Box Plot**: Distribution of all execution times

## Installation

1. Ensure PostgreSQL is running with the `cm_numbers` database
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Verify your `.env` file contains database credentials:

```
DB_HOST=localhost
DB_NAME=cm_numbers
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

## Usage

### Basic Usage

Run with default settings (5 runs per test):

```bash
python run_performance_tests.py
```

### Advanced Usage

Customize number of test runs:

```bash
python run_performance_tests.py --runs 10
```

Specify custom test directory:

```bash
python run_performance_tests.py --testing-dir ../testing
```

Skip visualizations (faster, for quick tests):

```bash
python run_performance_tests.py --no-viz
```

Change output directory:

```bash
python run_performance_tests.py --output-dir results_2024
```

### Full Options

```bash
python run_performance_tests.py --help
```

## Output

The framework generates several output files in `performance_results/`:

### CSV Results

- `results_YYYYMMDD_HHMMSS.csv`: Detailed timing data for all tests

**CSV Columns:**
- `test_file`, `line`, `num_factors`, `factors`: Test case info
- `Single Table_mean_ms`, `Single Table_median_ms`, etc.: Single table stats
- `Multi-Table (Partitioned)_mean_ms`, etc.: Multi-table stats
- `speedup`: Ratio of performance (>1 means multi-table is faster)

### Visualizations

1. `comparison_bar_chart.png`: Bar chart comparing execution times
2. `speedup_chart.png`: Speedup visualization (green = faster, red = slower)
3. `factor_count_analysis.png`: Line chart showing performance vs. factor count
4. `distribution_box_plot.png`: Box plots of execution time distributions

## Test Cases

Test cases are stored in the `testing/` directory:

- `2_composites.txt`: Numbers with 2 prime factors
- `3_composites.txt`: Numbers with 3 prime factors
- `4_composites.txt`: Numbers with 4 prime factors
- `5_composites.txt`: Numbers with 5 prime factors
- `6_2_unbalanced.txt`: Unbalanced 2-factor numbers
- `7_3_unbalanced.txt`: Unbalanced 3-factor numbers

(Note: `1_primes.txt` is excluded from testing as specified)

## Extending the Framework

### Adding a New Database Implementation

1. Create a new class inheriting from `CarmichaelDatabase`
2. Implement the required methods:
   - `query_by_factors()`
   - `get_implementation_name()`
   - `get_table_info()`
3. Add it to the `databases` list in `run_performance_tests.py`

Example:

```python
class CustomDB(CarmichaelDatabase):
    def get_implementation_name(self) -> str:
        return "Custom Implementation"

    def get_table_info(self) -> str:
        return "Custom table structure description"

    def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]:
        # Your custom query logic here
        pass
```

### Adding Custom Visualizations

Add new methods to the `PerformanceVisualizer` class in `visualizer.py`:

```python
def plot_custom_chart(self, stats: Dict[str, List[TestRunStats]], filename: str):
    # Your visualization code here
    pass
```

Then call it in `generate_all_visualizations()`.

### Modifying Test Runs

The number of test runs can be changed:

1. **Command line**: `--runs N`
2. **Programmatically**: `TestRunner(num_runs=N)`
3. **Default**: Change `default=5` in the argument parser

## Performance Metrics

The framework tracks these metrics for each query:

- **Mean Time**: Average execution time across all runs
- **Median Time**: Middle value (less affected by outliers)
- **Min Time**: Best case performance
- **Max Time**: Worst case performance
- **Standard Deviation**: Measure of consistency
- **Speedup**: Performance ratio between implementations

## Troubleshooting

### Connection Errors

If you see database connection errors:

1. Verify PostgreSQL is running
2. Check `.env` file credentials
3. Ensure `cm_numbers` database exists
4. Verify tables are populated with data

### Import Errors

If you get module import errors:

```bash
pip install -r requirements.txt
```

### Visualization Errors

If matplotlib fails to generate charts:

```bash
pip install --upgrade matplotlib
```

Or run tests without visualizations:

```bash
python run_performance_tests.py --no-viz
```

## Example Output

```
================================================================================
CARMICHAEL NUMBER DATABASE PERFORMANCE TESTING
================================================================================
Test runs per query: 5
Test directory: testing
Output directory: performance_results
Start time: 2024-11-14 15:30:00
================================================================================

[1/5] Loading test cases...
Loaded 50 test cases from 6 files:
  - 2_composites.txt: 15 cases
  - 3_composites.txt: 10 cases
  ...

[2/5] Initializing database connections...
  - Single Table: Table: carmichael_number (all factors in one table)
  - Multi-Table (Partitioned): Tables: carmichael_number_3 through carmichael_number_14

[3/5] Running performance tests...
This will execute 500 queries total

Test: 2_composites.txt:L1 (factors: [11, 13])
[1/100] Testing with Single Table...
  Completed 5 runs
  Single Table: mean=2.34ms, median=2.31ms, min=2.28ms, max=2.45ms, std=0.07ms
[2/100] Testing with Multi-Table (Partitioned)...
  Completed 5 runs
  Multi-Table (Partitioned): mean=1.87ms, median=1.85ms, min=1.82ms, max=1.95ms, std=0.05ms

...

[4/5] Generating summary...
================================================================================
PERFORMANCE TEST SUMMARY
================================================================================

Single Table:
  Total tests: 50
  Total time (mean): 125.34ms
  Average time per query: 2.51ms

Multi-Table (Partitioned):
  Total tests: 50
  Total time (mean): 98.76ms
  Average time per query: 1.98ms

Overall Speedup: 1.27x
Multi-Table (Partitioned) is 1.27x faster
================================================================================

[5/5] Generating visualizations...
Saved bar chart to performance_results/comparison_bar_chart.png
Saved speedup chart to performance_results/speedup_chart.png
Saved factor count analysis to performance_results/factor_count_analysis.png
Saved box plot to performance_results/distribution_box_plot.png
```

## Future Enhancements

Possible extensions to this framework:

1. **Query Types**: Add range queries, partial factor matching
2. **Concurrency Testing**: Test performance under concurrent load
3. **Memory Profiling**: Track memory usage in addition to time
4. **Database Indexing**: Compare different index strategies
5. **Caching**: Test impact of query result caching
6. **Statistical Analysis**: Add confidence intervals, hypothesis testing

## License

This testing framework is part of the CPSC571 Carmichael Storage project.
