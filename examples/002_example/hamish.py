import tree_maker, json
import pandas as pd
from rich.progress import track, Progress
import termplotlib as tpl
import numpy as np
import plotext as plt


def read_json(file_name):
    """
    Reads a json file and returns it in python.
    """
    with open(file_name) as json_file:
        json_object = json.load(json_file)
    return json_object


def plot_df(df, set_minimum_time=True):
    """
        Plots the columns of a dataframe. Either all of the columns in the dataframne can be plotted at once, or specific columns can be plotted seperately. For the example we will look at a datafraame with four columns: mutated, submitted, started and completed.

    Examples
    --------
    >>>plot_df(my_dataframe)

    This will return a plot of all four columns.

    >>>plot_df(my_dataframe['completed'])

    This will return a plot of only the column 'completed'.
    """
    if set_minimum_time == True:
        df = (df - df.min().min()) / 1e9
    for my_column in df.columns:
        y = df[my_column]
        plt.scatter(y)
        plt.plotsize(100, 30)
        plt.title(f"{my_column}")
        plt.xlabel("number of jobs")
        plt.ylabel("time (s)")
    plt.show()


def return_dataframe(node_list):
    """
    Returns a formatted pandas dataframe.
    """
    my_list = []
    for my_node in node_list:
        my_list.append(read_json(my_node.log_file))
    return pd.DataFrame(my_list)


def add_duration(df):
    """
    Adds a duration column to the dataframe, which is the time a job takes to be completed after it is started.
    """
    df["duration"] = df["completed"] - df["started"]


def add_pending(df):
    """
    Adds a pending column to the dataframe, which is the time a job takes to start after it has been submitted.
    """
    df["pending"] = df["started"] - df["submitted"]


def show_progress(df):
    """
    Shows the progress of the jobs which are running. It returns a set of progress bars corresponding to the status of the different jobs. So it would return progress bars for 'mutated', submitted' etc.
    """
    with Progress() as progress:
        tasks = []
        for my_column in df.columns:
            tasks.append(
                progress.add_task(
                    f"{my_column}...{len(df[my_column].dropna())}/{len(df)}",
                    total=len(df),
                )
            )

        for my_index, my_column in enumerate(df.columns):
            progress.update(tasks[my_index], completed=len(df[f"{my_column}"].dropna()))


if __name__ == "__main__":
    root = tree_maker.tree_from_json(f"./study_000/tree.json")
    my_df = return_dataframe(root.generation(1))
    plot_all(my_df)
