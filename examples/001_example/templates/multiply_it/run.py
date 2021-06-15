import json
import numpy as np
import ruamel.yaml
import tree_maker

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)

tree_maker.tag.tag_it(cfg['log_file'], 'started')
    
# define the function (product of two numbers)
def my_function(my_x, my_y):
    'Just a multiplication'
    return my_x*my_y

# run the code
result = my_function(cfg['sum_a_b'], cfg['c'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)
    
tree_maker.tag.tag_it(cfg['log_file'], 'completed')

