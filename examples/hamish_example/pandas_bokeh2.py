import pandas_skeleton as ps
import tree_maker as tm
from pandas import DataFrame

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, WheelZoomTool, BoxZoomTool, Button, PanTool
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook

output_notebook()

#root = tm.tree_from_json(filename='/home/HPC/sterbini/DA_study_example/study_000/tree.json')

def bkapp(doc, root, last_key, choose_color):
    """
    This creates an interactive plot showing a tree of jobs in a 'flower' shape.
    """
    global my_df
    global source1
    global source2
    
    try:
        ps.create_tree(root)
    except:
        raise Exception('Sorry, I need a root of a tree!')
        
    x_values, y_values, path = ps.create_xypath(root)
    my_colors = ps.create_color(root)
    angles = ps.create_tree_cartesian(root)
    
    my_df = ps.create_df(root, path, x_values, y_values, my_colors)
    
    del my_df['handle']
    
    def callback(attr, index_list, _):
        global my_df
        global my_df_selected
        source1.data = ColumnDataSource.from_df(my_df[my_df.status == last_key])
        source2.data = ColumnDataSource.from_df(my_df[my_df.status != last_key])
        my_df_selected = my_df.loc[index_list]

    def dummyfunction():
        global my_df
        my_df = ps.update(my_df, last_key, choose_color)
    
    dummyfunction()
    
    source1 = ColumnDataSource(data=my_df[my_df.status == last_key])
    source2 = ColumnDataSource(data=my_df[my_df.status != last_key])
    
    TOOLTIPS = [
    ('index', "@index"),
    ('status', "@status"),
    ('path', "@path")
]
    plot = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here", tooltips = TOOLTIPS)
    plot.circle('x', 'y', source=source1, alpha=0.6, color = 'color', legend_label = last_key)
    plot.circle('x', 'y', source=source2, alpha=0.6, color = 'color', legend_label = f'not {last_key}')
    plot.add_tools(BoxZoomTool(), WheelZoomTool(), PanTool())
    plot.legend.location = "top_left"
    plot.legend.click_policy="hide"
    
    source1.selected.on_change('indices', callback)
    source2.selected.on_change('indices', callback)

    button = Button(label="Update", button_type="success")

    button.on_click(dummyfunction)

    doc.add_root(column(plot, button))
    