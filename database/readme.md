# Database Setup Instructions
0. Ensure the requirements from `requirements.txt` are installed.
1. Create database in Postgres.
2. Setup connection details inside the .env file. The file should be located in the root directory of this project.
3. Run `create_tables.sql`.
    a. For the most absolute optimized run time, create the carmichael_number table first, then insert the first batch of data with `python copy_data_one_table.py`, then run the remaining scripts.
4. Run:
    `python copy_data_one_table.py` <br>
    `python copy_data_factor_tables.py`.