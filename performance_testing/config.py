"""
Configuration settings for performance testing.

Modify these values to customize test behavior without changing code.
"""

# Test execution settings
DEFAULT_NUM_RUNS = 5  # Number of times to run each test
TESTING_DIR = "testing"  # Directory containing test case files
OUTPUT_DIR = "performance_results"  # Directory for output files

# Database connection settings (override .env if needed)
# Leave as None to use values from .env file
DB_HOST = None
DB_NAME = None
DB_USER = None
DB_PASSWORD = None
DB_PORT = None

# Visualization settings
CHART_DPI = 300  # Resolution for saved charts (higher = better quality)
CHART_STYLE = 'default'  # Matplotlib style: 'default', 'seaborn', 'ggplot', etc.

# Test filtering (optional)
# Specify which test files to include/exclude
INCLUDE_TEST_FILES = None  # None = all files, or list like ['2_composites.txt']
EXCLUDE_TEST_FILES = ['1_primes.txt']  # Files to always exclude

# Performance testing options
WARMUP_RUNS = 0  # Number of warmup runs before actual measurement (not counted)
ENABLE_QUERY_CACHE = False  # Whether to clear query cache between tests

# Reporting options
VERBOSE_OUTPUT = True  # Print detailed progress during tests
SAVE_RAW_RESULTS = True  # Save raw timing data in addition to summary
TIMESTAMP_FILES = True  # Add timestamp to output filenames

# Chart colors (customize visualization appearance)
CHART_COLORS = {
    'single_table': '#3498db',  # Blue
    'multi_table': '#e74c3c',   # Red
    'faster': '#2ecc71',         # Green
    'slower': '#e74c3c',         # Red
}
