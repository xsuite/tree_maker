# %%
"""
Example of a chronjob
"""

# %%
import tree_maker
from tree_maker import NodeJob
import pandas as pd
import awkward as ak
import os

#from dask import dataframe as dd
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
    for node in root.generation(1):
        node.tag_as('postprocessing_submitted')
        node.submit_command=f'bsub -q hpc_acc {node.template_path}/postprocess.sh &'
        node.submit()
else:
    print('Complete first all jobs')

