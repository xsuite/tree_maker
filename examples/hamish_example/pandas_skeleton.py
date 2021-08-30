import tree_maker as tm
import numpy as np
import math
import random
from anytree import AnyNode, RenderTree
import numpy as np
import json
import pandas as pd

def create_tree(node):
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
            create_tree(my_child)
            
            
def create_xypath(node):
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

def create_color(node):
    """
    Adds colors of nodes to an array.
    """
    my_colors = [node.color]
    for descendant in node.descendants:
        my_colors.append(descendant.color)
    return my_colors

def create_tree_cartesian(node):
    """
    Adds the angle attribute to an array.
    """
    angles = [node.angle]
    for descendant in node.descendants:
        angles.append(node.angle)
    return angles

def get_status(handle):
    """
    Returns last key, the status of the job, from 'log_file'. Incase of an empty log_file, 'None' is returned.
    """
    keys = list(tm.from_json(handle.log_file))
    if len(keys) > 0:
        return keys[-1]
    else:
        return None
    
def create_df(node, path, x_values, y_values, my_colors):
    """
    Creating a dataframe and its attributes. Here its attributes are; node, path, x_values, y_values and my_colors.
    """
    my_df = pd.DataFrame([node]+list(node.descendants), columns=['handle']).copy()
    my_df['name'] = my_df['handle'].apply(lambda x:x.name)
    my_df['path'] = path
    my_df['x'] = x_values # to check the order
    my_df['y'] = y_values # to check the order
    my_df['status'] = my_df['handle'].apply(get_status)
    my_df['color'] = my_colors
    return my_df

def update(my_df, last_key, my_color):
    """
    Filtering through the dataframe using the 'last_key'. The color that is connected to this 'last_key', can also be chosen.
    """
    new_df1 = my_df[(my_df.status == last_key)].copy()
    new_df1['color'] = my_color
    new_df2 = my_df[(my_df.status != last_key)].copy()
    my_df = pd.concat([new_df1, new_df2]).sort_index()
    return my_df