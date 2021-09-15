import pandas_skeleton as ps
import tree_maker as tm
from pandas import DataFrame

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, WheelZoomTool, BoxZoomTool, Button, PanTool
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook
from bokeh.models import Select

def bkapp(doc, root, last_key, my_dict):
    """
    This creates an interactive plot showing a tree of jobs in a 'flower' shape.
    """
    global my_df
    global source
    global this_df
    global my_df_plot
    
    try:
        ps.create_tree(root)
    except:
        raise Exception('Sorry, I need a root of a tree!')
        
    x_values, y_values, path = ps.create_xypath(root)
    my_colors = ps.create_color(root)
    angles = ps.create_tree_cartesian(root)
    
    my_df = ps.create_df(root, path, x_values, y_values, my_colors)
    
    del my_df['handle']
    
    my_df_plot = my_df
    
    this_df = my_df.copy()
    
    final_status = my_dict['status'][-1]
    
    def callback(attr, _, index_list):
        global my_df
        global my_df_selected
        global my_df_plot
        source.data = ColumnDataSource.from_df(my_df_plot)
        my_df_selected = my_df_plot.loc[index_list]

    def initialise():
        global my_df_plot
        global my_df
        my_df_plot = ps.update_color(this_df, my_dict, my_df)
        my_df = ps.update_color(this_df, my_dict, my_df)
    
    def my_function(this_df, my_dict):
        return my_dict['color'][my_dict['status'].index(this_df['status'])]
    
    def update_color():
        global my_df_plot
        global my_df
        ps.update_status(root)
        this_df['status'] = ps.create_status(root)
        this_df['color'] = this_df.apply(lambda x: my_function(x, my_dict), axis=1)
        my_df = this_df
        my_df_plot = this_df

    def update_color2():
        global my_df_plot
        global my_df
        ps.update_status(root)
        this_df['status'] = ps.create_status(root)
        this_df['color'] = this_df.apply(lambda x: my_function(x, my_dict), axis=1)
        my_df = this_df
        my_df_plot = this_df
        source.data = ColumnDataSource.from_df(my_df_plot)

    update_color()
    
    source = ColumnDataSource(data=my_df_plot)
    
    TOOLTIPS = [
    ('index', "@index"),
    ('status', "@status"),
    ('path', "@path")
]
    plot = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here", tooltips = TOOLTIPS)
    plot.circle('x', 'y', source=source, alpha=0.6, size = 15, line_color="black", color = 'color')
    plot.add_tools(BoxZoomTool(), WheelZoomTool(), PanTool())

    source.selected.on_change('indices', callback)
    
    select = Select(title="Option:", value="plot", options=["full_df", f"{last_key}", f"not {last_key}"])

    def callback1(attr, old, new):
        global my_df_plot
        if new == "full_df":
            my_df_plot = my_df.copy()
        if new == f"{last_key}":
            my_df_plot = my_df[my_df.status == last_key].copy()
        if new == f"not {last_key}":
            my_df_plot = my_df[my_df.status != last_key].copy()
        my_df_plot.reset_index(drop=True, inplace=True)
        source.data = ColumnDataSource.from_df(my_df_plot)

    select.on_change('value', callback1)
    
    button = Button(label="Update", button_type="success")

    button.on_click(update_color2)

    doc.add_root(column(plot, button, select))