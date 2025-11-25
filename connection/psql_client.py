import subprocess
import os
from typing import Optional, Dict

class PSQLClient:
    """
    A client for executing PostgreSQL commands via subprocess using the psql CLI tool.

    This class abstracts away subprocess commands to connect to and interact with
    a PostgreSQL database, providing methods for queries and bulk inserts.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        port: Optional[str] = None
    ):
        """
        Initialize the PostgreSQL client with connection parameters.

        Args:
            host: Database host. If None, reads from HOST environment variable.
            database: Database name. If None, reads from DATABASE environment variable.
            user: Database user. If None, reads from PQ_USER environment variable.
            password: Database password. If None, reads from PQ_USER_PASSWORD environment variable.
            port: Database port. If None, reads from PQ_PORT environment variable.
        """
        self.host = host or os.getenv('HOST')
        self.database = database or os.getenv('DATABASE')
        self.user = user or os.getenv('PQ_USER')
        self.password = password or os.getenv('PQ_USER_PASSWORD', '')
        self.port = port or os.getenv('PQ_PORT')

        self._validate_connection_params()

    def _validate_connection_params(self):
        """Validate that all required connection parameters are set."""
        if not all([self.host, self.database, self.user, self.port]):
            missing = []
            if not self.host:
                missing.append('host')
            if not self.database:
                missing.append('database')
            if not self.user:
                missing.append('user')
            if not self.port:
                missing.append('port')
            raise ValueError(
                f"Missing required connection parameters: {', '.join(missing)}. "
                "Provide them as arguments or set environment variables."
            )

    def _build_base_command(self) -> list:
        """Build the base psql command with connection parameters."""
        return [
            'psql',
            '-h', self.host,
            '-U', self.user,
            '-d', self.database,
            '-p', self.port
        ]

    def _get_env_with_password(self) -> Dict[str, str]:
        """Get environment dict with PGPASSWORD set if password is available."""
        env = os.environ.copy()
        if self.password:
            env['PGPASSWORD'] = self.password
        return env

    def execute_query(
        self,
        query: str,
        input_data: Optional[str] = None,
        tuples_only: bool = True,
        unaligned: bool = True
    ) -> str:
        """
        Execute a SQL query using psql command-line tool.

        Args:
            query: SQL query to execute
            input_data: Optional data to pipe to stdin
            tuples_only: If True, returns tuples only without headers (-t flag)
            unaligned: If True, returns unaligned output (-A flag)

        Returns:
            Query output as a string

        Raises:
            Exception: If the psql command fails
        """
        cmd = self._build_base_command()

        if tuples_only:
            cmd.append('-t')
        if unaligned:
            cmd.append('-A')

        cmd.extend(['-c', query])

        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            env=self._get_env_with_password()
        )

        if result.returncode != 0:
            raise Exception(f"psql command failed: {result.stderr}")

        return result.stdout.strip()

    def copy_from_stdin(
        self,
        table_name: str,
        data: str,
        columns: Optional[tuple] = None
    ) -> None:
        """
        Insert data using COPY command via psql with data from stdin.

        Args:
            table_name: Name of the table to insert into
            data: Tab-separated values ready for COPY FROM STDIN
            columns: Optional tuple of column names. If None, uses all columns.

        Raises:
            Exception: If the COPY command fails
        """
        if columns:
            columns_str = f"({', '.join(columns)})"
        else:
            columns_str = ""

        copy_query = f'COPY {table_name} {columns_str} FROM STDIN'

        cmd = self._build_base_command()
        cmd.extend(['-c', copy_query])

        result = subprocess.run(
            cmd,
            input=data,
            capture_output=True,
            text=True,
            env=self._get_env_with_password()
        )

        if result.returncode != 0:
            raise Exception(f"COPY command failed: {result.stderr}")

    def execute_file(self, file_path: str) -> str:
        """
        Execute SQL commands from a file.

        Args:
            file_path: Path to SQL file

        Returns:
            Output from executing the file

        Raises:
            Exception: If the psql command fails
        """
        cmd = self._build_base_command()
        cmd.extend(['-f', file_path])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=self._get_env_with_password()
        )

        if result.returncode != 0:
            raise Exception(f"psql command failed: {result.stderr}")

        return result.stdout.strip()

    def execute_multiple_queries(self, queries: list) -> list:
        """
        Execute multiple SQL queries sequentially.
        """
        results = []
        for query in queries:
            results.append(self.execute_query(query))
        return results

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        """
        query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = '{table_name}'
        );
        """
        result = self.execute_query(query)
        return result.lower() == 't'
