import pandas_skeleton as ps
import tree_maker as tm
from pandas import DataFrame

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, WheelZoomTool, BoxZoomTool, Button
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook

output_notebook()

#root = tm.tree_from_json(filename='/home/HPC/sterbini/DA_study_example/study_000/tree.json')

def bkapp(doc):
    global my_df
    global source
    
    try:
        ps.create_tree(root)
    except:
        raise Exception('Sorry, I need a root of a tree!')
        
    x_values, y_values, path = ps.create_xypath(root)
    my_colors = ps.create_color(root)
    angles = ps.create_tree_cartesian(root)
    
    my_df = ps.create_df(root, path, x_values, y_values, my_colors)
    
    del my_df['handle']
    
    source = ColumnDataSource(data=my_df)

    plot = figure(plot_width=400, plot_height=400, tools="lasso_select", title="Select Here")
    plot.circle('x', 'y', source=source, alpha=0.6, color = 'color')
    plot.add_tools(BoxZoomTool())
    
    def callback(attr, index_list, _):
        global my_df
        global my_df_selected
        source.data = ColumnDataSource.from_df(my_df)
        my_df_selected = my_df.loc[index_list]

    def dummyfunction():
        global my_df
        my_df = ps.update(my_df, 'completed', 'green')

    source.selected.on_change('indices', callback)
    button = Button(label="Update", button_type="success")

    button.on_click(dummyfunction)

    doc.add_root(column(plot, button))
    
show(bkapp, notebook_url='http://localhost:8102', port=8202) # notebook_url="http://localhost:8888"