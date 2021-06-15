import json
import numpy as np
import ruamel.yaml

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)
    
# define the function (sum of two numbers)
def my_function(my_x, my_y):
    'Just an addition'
    return my_x+my_y

# run the code
result = my_function(cfg['a'], cfg['b'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)