import yaml

from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, WheelZoomTool, BoxZoomTool, Button
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.io import show, output_notebook
from pandas import DataFrame
import functions_imported_tree as fi
from functions_imported_tree import ColumnDataSource, TableColumn, DataTable, figure, CustomJS, row, show
import pandas as pd
import tree_maker as tm

output_notebook()

root = tm.tree_from_json(filename='/home/HPC/sterbini/DA_study_example/study_000/tree.json')

def bkapp(doc):
    global my_df
    global source
    
    fi.create_tree_flower(root)
    x_values, y_values, path = fi.create_xy(root)
    angles = fi.create_tree_cartesian(root)
    my_colors = fi.create_color(root)
    
    my_df = DataFrame([root]+list(root.descendants), columns=['handle']).copy() #I removed .copy(), is that a problem?
    
    my_df['name'] = my_df['handle'].apply(lambda x:x.name)
    my_df['path'] = path
    my_df['x'] = x_values # to check the order
    my_df['y'] = y_values # to check the order
    my_df['status'] = my_df['handle'].apply(fi.get_status)
    my_df['color'] = my_colors
    fi.color_from_status(my_df, 'completed')
    
    def update_on_click():
        global my_df
        new_df1 = my_df[(my_df.status == 'completed')].copy()
        new_df2 = my_df[(my_df.status != 'completed')].copy()
        my_df = pd.concat([new_df1, new_df2]).sort_index()
        
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
        
    source.selected.on_change('indices', callback)
    button = Button(label="Update", button_type="success")
    button.on_click(update_on_click)

    doc.add_root(column(plot, button))
    
show(bkapp, notebook_url='http://localhost:8102', port=8202) # notebook_url="http://localhost:8888"