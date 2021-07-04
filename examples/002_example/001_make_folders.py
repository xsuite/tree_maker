# %%
import tree_maker
from tree_maker import NodeJob
import time
# %%
# Clearly for this easy task on can do all in the very same python kernel
# BUT here we want to mimic the typical flow
# 1. MADX for optics matching/error seeding
# 2. Tracking for FMA and or DA studies
# 3. simulation baby-sitting and
# 4. postprocessing

import numpy as np
a=np.random.randn(50)
b=np.random.randn(50)
c=np.random.randn(10)

my_list_original=[]
for ii in c:
    my_list_original+=list(np.sqrt(np.abs((a+b)*ii)))
my_list_original=sorted(my_list_original)

# %%
"""
#### The root of the tree 
"""
start_time = time.time()
# %%
#root
import os
my_folder = os.getcwd()
root = NodeJob(name='root', parent=None)
root.path = my_folder + '/study_000'
root.template_path = my_folder + '/templates'
root.log_file = root.path + "/log.json"

# %%
"""
#### First generation of nodes
"""

# %%
#first generation
for node in root.root.generation(0):
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node,
                           path=f"{node.path}/{child:03}",
                           template_path = root.template_path+'/sum_it',
                           #submit_command = f'python {root.template_path}/sum_it/run.py &',
                           submit_command = f'bsub -q hpc_acc -e %J.err -o %J.out cd {node.path}/{child:03} && {root.template_path}/sum_it/run.sh &',
                           log_file=f"{node.path}/{child:03}/log.json",
                           dictionary={'a':float(a[child]), 
                                       'b':float(b[child])
                                      })
                   for child in range(len(a))]

# To combine different lists one can use the product or the zip functions    
#import itertools
#[[i, j, z] for i, j, z in itertools.product(['a','b'],['c','d'],[1,2,3])]
#[[i, j, z] for i, j, z in zip(['a','b'],['c','d'],[1,2,3])]

# %%
"""
#### Second generation of nodes
"""

# %%
#second generation
for node in root.root.generation(1):
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node,
                           path = f"{node.path}/{child:03}",
                           template_path = f'{root.template_path}/multiply_it',
                           #bsub -q hpc_acc -e %J.err -o %J.out cd $PWD && ./run.sh
                           submit_command = f'bsub -q hpc_acc -e %J.err -o %J.out cd {node.path}/{child:03} && {root.template_path}/multiply_it/run.sh &',
                           #submit_command = f'python {root.template_path}/multiply_it/run.py &',
                           log_file=f"{node.path}/{child:03}/log.json",
                           dictionary={'c': float(c[child])})
                   for child in range(len(c))]

root.to_json()


print('Done with the tree creation.')
print("--- %s seconds ---" % (time.time() - start_time))
# %%
"""
### Cloning the templates of the nodes
From python objects we move the nodes to the file-system.
"""

# %%
# We map the pythonic tree in a >folder< tree
start_time = time.time()
root.clean_log()
root.rm_children_folders()
from joblib import Parallel, delayed

for depth in range(root.height):
#    [x.clone_children() for x in root.generation(depth)]
     Parallel(n_jobs=8)(delayed(x.clone_children)() for x in root.generation(depth))

# VERY IMPORTANT, tagging
root.tag_as('cloned')
print('The tree structure is moved to the file system.')
print("--- %s seconds ---" % (time.time() - start_time))
