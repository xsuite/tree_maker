import json
import numpy as np
import ruamel.yaml
import tree_maker

# load the configuration
with open('config.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    cfg = yaml.load(file)
    
with open(cfg['parent']+'/output.yaml', 'r') as file:
    yaml = ruamel.yaml.YAML()
    parent_out = yaml.load(file)

tree_maker.tag_json.tag_it(cfg['log_file'], 'started')
    
# define the function (product of two numbers)
def my_function(my_x, my_y):
    'Just a multiplication'
    return my_x*my_y

# run the code
result = my_function(parent_out['result'], cfg['c'])

with open('output.yaml', 'w') as fp:
    yaml = ruamel.yaml.YAML()
    yaml.dump({'result': result}, fp)
    
import pandas as pd

pd.DataFrame(np.random.randn(100000,6), columns=['x','xp','y','yp','z','zp']).to_parquet('test.parquet', row_group_size=1000)

tree_maker.tag_json.tag_it(cfg['log_file'], 'completed')
