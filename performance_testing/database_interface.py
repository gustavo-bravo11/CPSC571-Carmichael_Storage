"""
Database Interface for Carmichael Number Storage Testing

This module provides an abstract interface for querying Carmichael numbers
from different database implementations (single table vs. partitioned tables).
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import subprocess
from decimal import Decimal
import os
from dotenv import load_dotenv
import json


class CarmichaelDatabase(ABC):
    """Abstract base class for Carmichael number database implementations."""

    def __init__(self):
        """Initialize database connection parameters using environment variables."""
        load_dotenv(override=True)
        self.host = os.getenv('HOST', 'localhost')
        self.database = os.getenv('DATABASE', 'cm_numbers')
        self.user = os.getenv('PQ_USER', 'postgres')
        self.password = os.getenv('PQ_USER_PASSWORD', '')
        self.port = os.getenv('PQ_PORT', '5432')

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass

    def close(self):
        """Close database connection (no-op for subprocess implementation)."""
        pass

    def run_psql_query(self, query):
        """
        Execute a SQL query using psql command-line tool.
        Returns the output as a string.
        """
        # Build psql command
        cmd = [
            'psql',
            '-h', self.host,
            '-U', self.user,
            '-d', self.database,
            '-p', self.port,
            '-t',  # Tuples only (no headers)
            '-A',  # Unaligned output
            '-c', query
        ]

        # Set password as environment variable
        env = os.environ.copy()
        if self.password:
            env['PGPASSWORD'] = self.password

        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env
        )

        if result.returncode != 0:
            raise Exception(f"psql command failed: {result.stderr}")

        return result.stdout.strip()

    @abstractmethod
    def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]:
        """
        Query for a Carmichael number containing the specified factors.

        Args:
            factors: List of prime factors to search for

        Returns:
            Tuple of (carmichael_number, full_factors_list) if found, None otherwise
        """
        pass

    @abstractmethod
    def get_implementation_name(self) -> str:
        """Return the name of this implementation for reporting."""
        pass

    @abstractmethod
    def get_table_info(self) -> str:
        """Return information about the table structure for reporting."""
        pass


class SingleTableDB(CarmichaelDatabase):
    """Implementation using a single carmichael_number table."""

    def get_implementation_name(self) -> str:
        return "Single Table"

    def get_table_info(self) -> str:
        return "Table: carmichael_number (all factors in one table)"

    def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]:
        """
        Query the single table for numbers containing all specified factors.

        Uses PostgreSQL array containment operator @> to find matching rows.
        """
        # Convert factors to array format for PostgreSQL
        factors_array = '{' + ','.join(str(f) for f in factors) + '}'

        query = f"""
            SELECT number, factors
            FROM carmichael_number
            WHERE factors @> '{factors_array}'::bigint[]
            LIMIT 1
        """

        result = self.run_psql_query(query)

        if result:
            # Parse the result (format: number|{factor1,factor2,...})
            lines = result.strip().split('\n')
            if lines and lines[0]:
                parts = lines[0].split('|')
                if len(parts) == 2:
                    number = Decimal(parts[0])
                    # Parse array format: {1,2,3} -> [1,2,3]
                    factors_str = parts[1].strip('{}')
                    factors_list = [int(f) for f in factors_str.split(',')]
                    return (number, factors_list)

        return None


class MultiTableDB(CarmichaelDatabase):
    """Implementation using partitioned tables (carmichael_number_3 to carmichael_number_14)."""

    def get_implementation_name(self) -> str:
        return "Multi-Table (Partitioned)"

    def get_table_info(self) -> str:
        return "Tables: carmichael_number_3 through carmichael_number_14 (partitioned by factor count)"

    def query_by_factors(self, factors: List[int]) -> Optional[Tuple[Decimal, List[int]]]:
        """
        Query partitioned tables for numbers containing all specified factors.

        Optimizes by only querying tables with factor count >= len(factors).
        This is the key optimization: we can skip tables with fewer factors.
        """
        num_factors = len(factors)

        # We can only have tables from 3 to 14 factors
        # Start searching from the minimum possible table
        start_table = max(3, num_factors)
        end_table = 14

        factors_array = '{' + ','.join(str(f) for f in factors) + '}'

        # Search tables in order from smallest to largest
        # This finds the first match with the minimum number of factors
        for factor_count in range(start_table, end_table + 1):
            table_name = f"carmichael_number_{factor_count}"

            query = f"""
                SELECT number, factors
                FROM {table_name}
                WHERE factors @> '{factors_array}'::bigint[]
                LIMIT 1
            """

            result = self.run_psql_query(query)

            if result:
                # Parse the result (format: number|{factor1,factor2,...})
                lines = result.strip().split('\n')
                if lines and lines[0]:
                    parts = lines[0].split('|')
                    if len(parts) == 2:
                        number = Decimal(parts[0])
                        # Parse array format: {1,2,3} -> [1,2,3]
                        factors_str = parts[1].strip('{}')
                        factors_list = [int(f) for f in factors_str.split(',')]
                        return (number, factors_list)

        return None
