import tree_maker as tm
import numpy as np
import math
import random
import bokeh
from bokeh.io import show, output_notebook
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import GraphRenderer, Ellipse, StaticLayoutProvider, HoverTool, Button, ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.palettes import Spectral8
from anytree import AnyNode, RenderTree
import numpy as np

from bokeh.resources import INLINE
bokeh.io.output_notebook(INLINE)
import json    

def create_tree_flower(node):
    """
    Creates a tree with the shape of a 'flower'. The nodes that have attributes; x, y, ragius, short_path, angle, min_angle, max_angle and color.
    """
    if node.is_leaf:
        pass
    else:
        if node.is_root:
            node.x = 0
            node.y = 0
            node.radius = 0
            #node.min_x = -2
            #node.max_x = 2
            node.short_path =  '/'.join(node.path.split('/')[-3:])
            node.angle = 2 * math.pi
            node.min_angle = 0
            node.max_angle = 2 * math.pi
            node.color = 'black'
        for my_child, my_angle in zip(node.children, np.linspace(node.min_angle, node.max_angle, len(node.children))):
            #my_child.min_x = xx - (node.max_x - node.min_x)/len(node.children)/2
            #my_child.max_x = xx + (node.max_x - node.min_x)/len(node.children)/2
            my_child.color = "black"
            my_child.short_path =  '/'.join(my_child.path.split('/')[-3:])
            my_child.angle = my_angle
            my_child.min_angle = my_angle - (node.max_angle - node.min_angle)/len(node.children)/2
            my_child.max_angle = my_angle + (node.max_angle - node.min_angle)/len(node.children)/2
            my_child.radius = node.radius + 1
            my_child.x = my_child.radius * math.cos(my_angle)
            my_child.y = my_child.radius * math.sin(my_angle)
            create_tree_flower(my_child)
            
def create_tree(node):
    """
    Creates a tree. The nodes that have attributes; x, min_x, max_x, y, ragius, short_path, angle, min_angle, max_angle and color.
    """
    if node.is_leaf:
        pass
    else:
        if node.is_root:
            node.x = 0
            node.y = 0
            node.min_x = -2
            node.max_x = 2
            node.short_path =  '/'.join(node.path.split('/')[-3:])
            node.angle = 2 * math.pi
            node.min_angle = 0
            node.max_angle = 2 * math.pi
            node.color = 'black'
        for my_child, xx, my_angle in zip(node.children, np.linspace(node.min_x, node.max_x, len(node.children)), np.linspace(node.min_angle, node.max_angle, len(node.children))):
            my_child.x = xx
            my_child.y = node.y - 1 
            my_child.min_x = xx - (node.max_x - node.min_x)/len(node.children)/2
            my_child.max_x = xx + (node.max_x - node.min_x)/len(node.children)/2
            my_child.color = "black"
            my_child.short_path =  '/'.join(my_child.path.split('/')[-3:])
            my_child.angle = my_angle
            my_child.min_angle = my_angle - (node.max_angle - node.min_angle)/len(node.children)/2
            my_child.max_angle = my_angle + (node.max_angle - node.min_angle)/len(node.children)/2
            create_tree(my_child)

            
def create_xy(node):
    """
    Creates a list for x_values and y_values for the nodes of a tree.
    """
    x_values = [node.x]
    y_values = [node.y]
    path = [node.short_path]
    for descendant in node.descendants:
        x_values.append(descendant.x) 
        y_values.append(descendant.y)
        path.append(descendant.short_path)
    return x_values, y_values, path

def color_from_status(my_df, last_key): # is this still relevant?
    my_df['color'] = 'green'
    #for index in my_df.index:
    #    if my_df['status'][index] == last_key:
    #        my_df['color'][index] = 'green'
    #    else:
    #        my_df['color'][index] = 'black'
            
def create_color(node):
    """
    Adds colors of nodes to an array.
    """
    my_colors = [node.color]
    for descendant in node.descendants:
        my_colors.append(descendant.color)
    return my_colors

#def create_tree_polar()

def create_tree_cartesian(node):
    """
    Adds the angle attribute to an array.
    """
    angles = [node.angle]
    for descendant in node.descendants:
        angles.append(node.angle)
    return angles

def read_json(path):
    """
    Returns a json file to read in python.
    """
    with open(path.log_file) as json_file:
        json_data = json.load(json_file)
    return json_data

def json_tree(node):
    
    my_dictionary = []
    for child in node.children:
        json_data = read_json(child)
        my_dictionary.append(json_data)
    return my_dictionary
    

def status_tree(node):
    for child in root.children:
        if len(read_json(child)) == 4:
            return child.color == 'red'

def get_color(handle):
    if handle.has_been('started'):
        my_color = 'red'
    if handle.has_been('completed'): 
        my_color = 'green'
    else:
        my_color = 'black'
    return my_color

def get_status(handle):
    """
    Returns last key, the status of the job, from 'log_file'.
    """
    keys = list(tm.from_json(handle.log_file))
    if len(keys) > 0:
        return keys[-1]
