import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def run_sql_file(sql_file_path):
    """
    Execute a SQL file using psql command-line tool.
    """
    # Build connection string
    host = os.getenv('HOST')
    database = os.getenv('DATABASE')
    user = os.getenv('PQ_USER')
    password = os.getenv('PQ_USER_PASSWORD', '')
    port = os.getenv('PQ_PORT')

    # Read the SQL file content
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Build psql command - execute SQL directly instead of using -f flag
    cmd = [
        'psql',
        '-h', host,
        '-U', user,
        '-d', database,
        '-p', port,
        '-c', sql_content
    ]

    # Set password as environment variable
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password

    # Run the command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        raise Exception(f"psql command failed: {result.stderr}")

    print(result.stdout)
    return result.stdout.strip()

def main():
    """
    Execute the create_tables.sql script to set up database tables.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, 'create_tables.sql')

    if not os.path.exists(sql_file):
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    print(f"Executing SQL file: {sql_file}")
    run_sql_file(sql_file)
    print("Tables created successfully!")

if __name__ == "__main__":
    main()
