import json
import numpy as np
import ruamel.yaml
import tree_maker

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)

tree_maker.tag.tag_it(cfg['log_file'], 'started')
    
# define the function (sum of two numbers)
def my_function(my_x, my_y):
    'Just an addition'
    return my_x+my_y

# run the code
result = my_function(cfg['a'], cfg['b'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)

tree_maker.tag.tag_it(cfg['log_file'], 'completed')