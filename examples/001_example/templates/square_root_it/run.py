import json
import numpy as np
import ruamel.yaml

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)
    
# define the function (sqrt of a number)
def my_function(my_x):
    'Just an addition'
    return float(np.sqrt(np.abs(my_x)))

# run the code
result = my_function(cfg['a'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)