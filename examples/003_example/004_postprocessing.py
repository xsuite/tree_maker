# %%
"""
Example of a chronjob
"""

# %%
import tree_maker
from tree_maker import NodeJob
import pandas as pd
import awkward as ak

# %%
# Load the tree from a yaml
try:
    root=tree_maker.tree_from_json(
    f'./study_000/tree.json')
except Exception as e:
    print(e)
    print('Probably you forgot to edit the address of you json file...')

my_list=[]
if root.has_been('completed'):
    print('All descendants of root are completed!')
    for node in root.generation(2)[0:100]:
        my_list.append(ak.from_parquet(f'{node.path}/test.parquet', columns=['x'], row_groups=99)['x',-1])
    print(my_list)
else:
    print('Complete first all jobs')

