"""
Database Interface for Carmichael Number Storage Testing

This module provides an abstract interface for querying Carmichael numbers
from different database implementations (single table vs. partitioned tables).
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
import os
from dotenv import load_dotenv


class CarmichaelDatabase(ABC):
    """Abstract base class for Carmichael number database implementations."""

    def __init__(self):
        """Initialize database connection using environment variables."""
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'cm_numbers'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        self.connection.autocommit = True

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        self.close()

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

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
        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            # Convert factors to array format for PostgreSQL
            factors_array = '{' + ','.join(str(f) for f in factors) + '}'

            query = """
                SELECT number, factors
                FROM carmichael_number
                WHERE factors @> %s::bigint[]
                LIMIT 1
            """

            cur.execute(query, (factors_array,))
            result = cur.fetchone()

            if result:
                return (result['number'], result['factors'])
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

        with self.connection.cursor(cursor_factory=RealDictCursor) as cur:
            factors_array = '{' + ','.join(str(f) for f in factors) + '}'

            # Search tables in order from smallest to largest
            # This finds the first match with the minimum number of factors
            for factor_count in range(start_table, end_table + 1):
                table_name = f"carmichael_number_{factor_count}"

                query = f"""
                    SELECT number, factors
                    FROM {table_name}
                    WHERE factors @> %s::bigint[]
                    LIMIT 1
                """

                cur.execute(query, (factors_array,))
                result = cur.fetchone()

                if result:
                    return (result['number'], result['factors'])

            return None
