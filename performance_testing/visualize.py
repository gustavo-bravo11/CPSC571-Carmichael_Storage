"""
Data Visualization File

This file will read the test results from sql_test.py and potentially other
files that are used for testing to then output the results into specialized
visualizations. All test results are compared against a baseline, which is
a text parser that was used prior to this. The baseline is hardcoded as a
constant, and then plotted on every graph that requires it.

By default we output two graphs, one with the baseline, and one without it.
This is done to adjust the scale of the y-axis to be more relevant if the
baseline is much higher than the total time of the tests.

The tests are first parsed from their text outputs, a specific
parser function is required for the specific test, and then the results
are appended into a pandas dataframe.

Then it will output the results of the visualizations as PNGs, with
the output pat specialized as a constant.

@author Gustavo Bravo
@date December 7, 2025
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json
import pandas as pd
import re

from pathlib import Path
from datetime import datetime
from math import ceil, log10

from matplotlib.axes import Axes
from matplotlib.colors import to_rgba

TEST_DIR = "database_results"
DATE = "2025-12-12"
IMG_DIR = "visualizations/" + DATE
ONE_TABLE_FILENAME = "one_table_results.txt"
MULTI_TABLE_FILENAME = "multi_table_results.txt"
MONGO_COLLECTION_FILENAME = "mongodb_results.txt"
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S-%f"
TEST_BASELINE_MS = 265000

image_counter = 0

plt.style.use('ggplot')
plt.rcParams.update({
    ''
    'font.size': 11,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'lines.linewidth': 2,
    'figure.facecolor': 'white',
    'axes.facecolor': to_rgba('lightsteelblue', 0.6),
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': 'black',
    'axes.linewidth': 1.2,
    'xtick.color': 'black',
    'ytick.color': 'black',
    'axes.labelcolor': 'black',
})

colours = {
    'C++ Parser': 'red',
    'One Table': 'blue',
    'Multi Table': 'darkorange',
    'Mongo DB': '#2f945b'
}


def create_grid(
        df:pd.DataFrame,
        title:str,
        subtitle:str,
        gb_col:str,
        val_col:str,
        improvement:bool = False,
    ) -> None:
    """
    Wrapper function for creating a grid of two visualizations.
    Creates one with a y title, legend, and baseline, and the second
    one does not include those attributes.

    @args:
        - df: A pandas dataframe with the data.
        - title: Display at the top of figure.
        - subtitle: Visualization description.
        - gb_col: Column name to group by.
        - val_col: Column name to aggregate.
        - improvement: If you are visualizing an improvement metric
    """

    if improvement:
        fig, axes = plt.subplots(1, 1, figsize=(5, 4))
        visualize(
            df=df,
            gb_col=gb_col,
            val_col=val_col,
            baseline=False,
            ax=axes
        )
    else:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        visualize(
            df=df,
            gb_col=gb_col,
            val_col=val_col,
            ax=axes[0]
        )
        visualize(
            df=df,
            gb_col=gb_col,
            val_col=val_col,
            baseline=False,
            y_label=False,
            legend=False,
            ax=axes[1]
        )

    fig.suptitle(title, fontsize=18, x=0, ha='left')
    fig.text(0, 0.875, subtitle, ha='left', fontsize=12, color='#2b2b2b')
    fig.subplots_adjust(top=0.85)

    global image_counter
    plt.savefig(
        f'{IMG_DIR}/{image_counter:02d}_{title.replace(' ','_').lower()}.png',
        dpi=300,
        bbox_inches='tight'
    )
    image_counter += 1


def visualize(
        df:pd.DataFrame,
        gb_col:str,
        val_col:str,
        baseline:bool = True,
        y_label:bool = True,
        legend:bool = True,
        agg_type:str = 'mean',
        ax:Axes=None,
    ) -> None:
    """
    Function created to visualize a variable specified.
    Uses a group by operation to group the schemas together,
    then it's aggregated by the passed in aggregation function,
        This must be a Pandas series function.

    There is a special case to show the baseline value if required.
        When this is false, it will omit showing the line,
        and the legend will also be omitted.

    This is meant to be used inside a mpl axis, the last
    argument shows this. If it is None, a new one is created.
    """
    if ax is None:
        ax = plt.subplot()

    for schema, group in df.groupby('schema'):
        avg_by_factors = group\
            .groupby(gb_col)[val_col]\
            .agg(agg_type)
        
        ax.plot(
            avg_by_factors.index, 
            avg_by_factors.values, 
            label=schema,
            color=colours.get(str(schema), 'black'),
            marker='.'
        )

    if baseline:
        ax.axhline(
            y=TEST_BASELINE_MS,
            color=colours.get('baseline', 'red'),
            linestyle='--',
            label='C++ Parser'
        )

    if legend:
        ax.legend(
            bbox_to_anchor=(1, 0.90),
            frameon=True,
            edgecolor='black',
            framealpha=0.8,
            facecolor='white',
        )

    if y_label:
        ax.set_ylabel(clean_names(avg_by_factors.name))

    # If the x labels are long we'll clean them and rotate for readability
    if max(len(str(label)) for label in df[gb_col].unique()) > 3:
        labels = [clean_names(str(label)) for label in df[gb_col].unique()]
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # If neither are true then this is a secondary viz
    # Therefore it has room for a subtitle
    # This just states the reason for removal
    if not baseline and not legend:
        ax.set_title("Observations without baseline", 
                     fontsize=12, loc='left', color='#2b2b2b')

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))    # Keeps the values as integers
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(ms_to_s))     # Converts the displayed amount to seconds from ms


def clean_names(name: str) -> str:
    """
    Helper function used to sanitize the column names for visualizing.
    """
    return name\
        .replace('_', ' ')\
        .replace('num', 'Number')\
        .replace('ms','')\
        .replace('.txt', '')\
        .strip().title()


def ms_to_s(val: int, pos:int) -> str:
    """
    Helper callback used to convert ms to s
    by Str formatter.
    """
    return f'{val/1000}s'


def display_summary_stats(df:pd.DataFrame) -> None:
    print("\nOverall statistic from all tests:")
    print("\nTable Averages")
    print(df.groupby(['schema'])['total_time_ms'].mean())
    print("\nTable Maximums")
    print(df.groupby(['schema'])['total_time_ms'].max())
    print("\nTable Minimums")
    print(df.groupby(['schema'])['total_time_ms'].min())
    print()


def collect_and_parse_data() -> list[list[dict]]:
    """
    Loop through the test directory, collect each folder name as the timestamp.
    Return the entirety of all the parsed data in the directory.
    """
    folder = Path(TEST_DIR)

    results = []
    for item in folder.iterdir():
        if not item.is_dir():
            continue
        
        # Only take the results from the day were interested on
        if not item.name.startswith(DATE):
            continue
        
        # Add the results from both schemata
        results += parse_SQL_explain(item / ONE_TABLE_FILENAME, item.name, "One Table")
        results += parse_SQL_explain(item / MULTI_TABLE_FILENAME, item.name, "Multi Table")
        results += parse_MDB_explain(item / MONGO_COLLECTION_FILENAME, item.name, "Mongo DB")
    
    return results


def parse_MDB_explain(
        path: Path, 
        test_timestamp: str, 
        testing_schema: str
    ) -> list[dict]:
    """
    NoSQL explain parser.

    NoSQL much cleaner as the results are returned as a JSON, with nested objects like this:
        {'executionSuccess': True,
        'filter': {'$and': [{'factor': {'$eq': 211}},
            {'factor': {'$eq': 1483}},
            {'factor': {'$eq': 4297}},
            {'factor': {'$eq': 7741}}]},
        'allPlansExecution': []}

    We are interested in getting the factors from the query, the optimization time
    and the execution time. The sum of these two is our total time.
    """
    results = []

    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    test_blocks = re.split(r"=+\s*TEST_NAME:", text)[1:]
    for block in test_blocks:
        name_match = re.search(r"(.*?)\n=+", block)
        test_name = name_match.group(1).strip() if name_match else None

        case_blocks = re.split(r"=+\s*TEST_CASE_NUM:", block)[1:]

        for case_block in case_blocks:
            case_match = re.search(r"(\d+)", case_block)
            case_num = int(case_match.group(1)) if case_match else None

            # Parse the json results from the .explain query
            json_start = case_block.find('\n', case_block.find('='))
            data = json.loads(case_block[json_start:].strip()) if json_start else None

            planning_time = float(data['queryPlanner']['optimizationTimeMillis']) if data else None
            execution_time = float(data['executionStats']['executionTimeMillis']) if data else None

            parsed_query = data['queryPlanner']['parsedQuery'] if data else None

            # Multi case if there are multiple factors
            if parsed_query:
                if '$and' in parsed_query:
                    factors_str = ','.join(
                        str(e['factors']['$eq']) for e in parsed_query['$and']
                    )
                else:
                    factors_str = str(parsed_query['factors']['$eq'])
            else:
                factors_str = None

            results.append({
                "schema": testing_schema,
                "timestamp": datetime.strptime(test_timestamp, TIMESTAMP_FORMAT),
                "name": test_name,
                "case_num": case_num,
                "factors": factors_str,
                "total_time_ms": planning_time + execution_time if planning_time is not None and execution_time is not None else None
            })
        
    return results


def parse_SQL_explain(
        path: Path, 
        test_timestamp: str, 
        testing_schema: str
    ) -> list[dict]:
    """
    Parse the results of the tests analyze splitting the file into individual
    test blocks, and then looking for key elements in the text.

    What we are interested in;
        - The planning time,
        - The execution time, and
        - The time of algorithm used.

    The last one becomes tricky to implement since the UNION query uses multiple
    algorithms per part of the UNION, so we'll omit it for now.

    Returns, a list of dictionaries of the data parsed.
    """
    results = []
    
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    test_blocks = re.split(r"=+\s*TEST_NAME:", text)[1:]
    for block in test_blocks:
        name_match = re.search(r"(.*?)\n=+", block)
        test_name = name_match.group(1).strip() if name_match else None

        case_blocks = re.split(r"=+\s*TEST_CASE_NUM:", block)[1:]

        for case_block in case_blocks:
            case_match = re.search(r"(\d+)", case_block)
            case_num = int(case_match.group(1)) if case_match else None

            factors_match = re.search(r"({[\d,]*\d})", case_block)
            factors_str = factors_match.group(1).strip("{}") if factors_match else None

            plan_match = re.search(r"Planning Time:\s*([\d.]+)\s*ms", case_block)
            planning_time = float(plan_match.group(1)) if plan_match else None

            exec_match = re.search(r"Execution Time:\s*([\d.]+)\s*ms", case_block)
            execution_time = float(exec_match.group(1)) if exec_match else None

            results.append({
                "schema": testing_schema,
                "timestamp": datetime.strptime(test_timestamp, TIMESTAMP_FORMAT),
                "name": test_name,
                "case_num": case_num,
                "factors": factors_str,
                "total_time_ms": planning_time + execution_time if planning_time is not None and execution_time is not None else None
            })

    return results


def transform_data(df:pd.DataFrame) -> None:
    """
    Add columns for visualizing!

    DataFrame's are not primative types, therefore, they are edited in
    memory. Nothing to return.
    """
    df["improvement_ms"] = TEST_BASELINE_MS - df["total_time_ms"]
    df["improvement_percent"] = df["improvement_ms"] / TEST_BASELINE_MS
    df["num_of_factors"] = df["factors"].str.count(",") + 1

    # Get the min magnitude and max magnitude of each number in the tests
    df["min_ord_mag10"] = df["factors"].apply(
        lambda x: ceil(log10(min([int(p) for p in x.split(",")])))
    )
    df["max_ord_mag10"] = df["factors"].apply(
        lambda x: ceil(log10(max([int(p) for p in x.split(",")])))
    )

    # Balanced if the order of magnitudes equal from min to max
    df["balanced"] = df.apply(
        lambda x: "Balanced" if x["min_ord_mag10"] == x["max_ord_mag10"] else "Unbalanced",
        axis=1
    )

    # Sort the table by timestamp (asc), name (asc), case_num (asc), schema (asc)
    df.sort_values(
        ["timestamp", "name", "case_num", "schema"], 
        ascending=[True, True, True, False], 
        ignore_index=True,
        inplace=True, 
    )

    print("\nShowing the first 5 rows after transforming.")
    print(df.head())


def main():
    """
    This script will:
        - Parse the data from the explain analyze queries. The name of the
          directory indicates when the test was ran. Everything else will be
          collected from inside the file itself.
        - Organize the data onto a pandas dataframe with appropriate typing.
          This step also adds additional columns to the dataframe for
          analysis.
        - Visualize the results, comparing them against the baseline of
          4m:25s or 265000ms.

    The visualizations will be outputted onto PNGs to be used in the final
    report. The console will also output some summary statistics to give
    the user a brief preview of how the tests faired.
    """
    print("Analyzing database tests ran.")
    print(f"Comparing against the baseline of {TEST_BASELINE_MS:,}ms.")

    Path(IMG_DIR).mkdir(parents=True, exist_ok=True)
    results_df = pd.DataFrame(collect_and_parse_data())

    transform_data(results_df)

    display_summary_stats(results_df)

    # Create some visualizations!
    create_grid(results_df, "Total Time by Test", 
                "Average taken by group", 'name', 'total_time_ms')
    create_grid(results_df, "Test Improvement", 
                "Average taken by group", 'name', 'improvement_ms', True)

    create_grid(results_df, "Total Time by Number of Factors", 
                "Average taken by group", 'num_of_factors', 'total_time_ms')
    create_grid(results_df, "Factor Improvement", 
                "Average taken by group", 'num_of_factors', 'improvement_ms', True)

    balanced_df = results_df.query("balanced == 'Balanced'")
    create_grid(balanced_df, "Total Time By Orders of Magnitude (10)", 
                "Average taken for balanced tests", 'min_ord_mag10', 'total_time_ms')
    create_grid(balanced_df, "Order of Magnitude Improvement", 
                "Average taken by group", 'min_ord_mag10', 'improvement_ms', True)
    
    
if __name__ == "__main__":
    main()