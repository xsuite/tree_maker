# %%
"""
### Introduction

See https://codimd.web.cern.ch/p/0QX9ebi1bn#/ for the latest version.

Our community is often confronted with the need of running complex algorithms for a set of different input.
E.g. a DA computation with tune scan + beam-beam + errors.

This implies to stage the algorithm in different steps corresponding, sometimes, to different codes (MADX, SixTrack,...) and/or different hardware (local CPU, GPU, HTCondor/LSF clusters, BOINC...).

The topic of this brainstorming is to discuss about a python package that could convey a **standard** approach in order to

- avoid re-inventing the wheel each time, 
- improve the way we share our work-flow for the different simulations,
- provide a standard way to babysitting the simulations and postprocess the output.

Clearly the package can be integrated with other solutions (see next [presentation]()).

The challenge here is to maintain a good balance between simplicity (to be user-friendly) and flexibility (to cover a large gamut of use cases).

You can find at https://gitlab.cern.ch/abpcomputing/sandbox/tree_maker a proposal.
We are going first to present its rationale (a bit abstract, 5 min) and then explore together a simple example (pragmatic and complementary to the first part, 15 min).


### Rationale

The general way to describe our problem (running a staged algorithm for a set of different input) is to associate a **job** for each stage and input.

A job can be represented as a **node** in a **graph** (nodes connected with edges).
 
The main idea is to downscale the problem of a generic graph to a simpler graph, a **tree**.

A **tree** is a simplified [**DAG**](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (Directed Acycled Graphs) where each node can have maximum one parent.
The tree is convenient since it can be directly mapped into a file system (the folder stucture of a file system is a tree).

In python a tree can be represented, for example, with the `anytree` package (see [000_example](https://gitlab.cern.ch/abpcomputing/sandbox/tree_maker/-/blob/master/examples/000_example/000.ipynb)). 

The `anynode` object of the `anytree` package can be generalized to any class.
Indeed we generalized it to our `NodeJob` class, inheriting all the methods/attributes of `anynode`, e.g., root, parent, children, ancestors, siblings, leaves, depth, height, searching/filtering methods... 

The main ideas is that each node of our simulation tree 

1. is a instance of the `NodeJob` (extending the `anytree`).
2. refers to a **template node** (example a MadX mask): `NodeJob.template_path`
3. has a specific dictionary of input, `NodeJob.dictionary`
4. is mapped to a file system, `NodeJob.path`
5. has a specific submit command, `NodeJob.submit_command`
6. has a specific log file, `NodeJob.log_path`


The users should spend 99% of their time on the physics (the templates, each template is well "isolated" for a deep understanding of its physics), and use the package to build/orchestrate the tree.

#### Building of the tree
The building of the tree is done in three steps:
- istantiating the nodes
- **cloning** (i.e. copying) the templates on the NodeJob.path
- **mutating** (i.e. changing) the input of the template with the info in the NodeJob.dictionary


#### Orchestrating the tree

Each node can be run (refers to NodeJob.submit_command) and logged (NodeJob.submit_command).
One can orchestrate the simulation but writing and reading in the different log.

We will show now a simple example to clarify all these ingredients.
In this way we can factorize the physics (the template), the parameters (the dictionary), the folder (JobNode.path) but maintaining for all nodes the very same interface (`JobNode`).




### Simple example ([001_example](https://gitlab.cern.ch/abpcomputing/sandbox/tree_maker/-/blob/master/examples/001_example/001.ipynb))


Let aussume that we need to make this computation

$\sqrt{|(a+b)\times c|}$

and we want to compute the standard deviation of the result assuming that a, b and c are normal distributed independent variables. Clearly the problem is quite naive but we want to address it as if we will need a cluster to solve it. 

For example, we can partition the problem in three conscutive stages

1. A sum: $(a+b)$
2. A multiplication of the result 1 with c: $(a+b)\times c$
3. A sqrt of the result of 2: $\sqrt{|(a+b)\times c|}$

For each stage we build a template.
Documentation (only started, you need to be on GPN) can be found at https://acc-py.web.cern.ch/gitlab/abpcomputing/sandbox/tree_maker/docs/master/. 
"""

# %%
import tree_maker
from tree_maker import NodeJob

# %%
# Clearly for this easy task on can do all in the very same python kernel
# BUT here we want to mimic the typical flow
# 1. MADX for optics matching/error seeding
# 2. Tracking for FMA and or DA studies
# 3. simulation baby-sitting and
# 4. postprocessing

import numpy as np
a=np.random.randn(4)
b=np.random.randn(4)
c=np.random.randn(2)

my_list_original=[]
for ii in c:
    my_list_original+=list(np.sqrt(np.abs((a+b)*ii)))
my_list_original=sorted(my_list_original)

# %%
"""
#### The root of the tree 
"""

# %%
#root
root = NodeJob(name='root', parent=None)
root.path = '/home/jovyan/local_host_home/CERNBox/2021/tree_maker/examples/001_example/study_000'
root.template_path = root.path + '/../templates'
root.log_file = root.path + "/log.yaml"

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
                           submit_command = f'python run.py',
                           log_file=f"{node.path}/{child:03}/log.yaml",
                           dictionary={'a':float(a[child]), 
                                       'b':float(b[child])
                                      })
                   for child in range(len(a))]

# To combine different lists one can use the product or the zip functions    
#import itertools
#[[i, j, z] for i, j, z in itertools.product(['a','b'],['c','d'],[1,2,3])]
#[[i, j, z] for i, j, z in zip(['a','b'],['c','d'],[1,2,3])]
root.print_it()

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
                           template_path = root.template_path+'/multiply_it',
                           submit_command = f'python run.py',
                           log_file=f"{node.path}/{child:03}/log.yaml",
                           dictionary={'c': float(c[child])})
                   for child in range(len(c))]
root.print_it()

# %%
"""
#### Third generation of nodes
"""

# %%
#third generation
for node in root.root.generation(2):
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node, 
                           path = f"{node.path}/{child:03}",
                           template_path = root.template_path+'/square_root_it',
                           submit_command = f'python run.py',
                           log_file=f"{node.path}/{child:03}/log.yaml",
                           dictionary={'log_file': f"{node.path}/{child:03}/log.yaml"})
                           for child in range(1)]
root.print_it()

# %%
# we can inspect the data structure
root.children[3].children[1].children[0].submit_command

# %%
# or we can modify the attributes of the tree
if False:
    for i, node in enumerate(root.leaves):
        if i>3:
            print(i)
            node.submit_command = f'condor_submit run.sub -batch-name square_root'

# %%
# we can transfer the information of the tree in a yaml for the orchestration later
root.to_yaml()

# %%
"""
### Cloning the templates of the nodes
From python objects we move the nodes to the file-system.
"""

# %%
# We map the pythonic tree in a >folder< tree
root.clean_log()
root.rm_children_folders()
for depth in range(root.height):
    [x.clone_children() for x in root.generation(depth)]

# VERY IMPORTANT, tagging
root.tag_as('cloned')

# %%
"""
### Launching the jobs
"""

# %%
root.tag_as('launched')
for node in root.generation(1):
    node.cleanlog_mutate_submit()

# %%
for node in root.generation(2):
    node.cleanlog_mutate_submit()

# %%
for node in root.generation(3):
    node.cleanlog_mutate_submit()

# %%
# check if all root descendants are completed 
if all([descendant.has_been('completed') for descendant in root.descendants]):
    root.tag_as('completed')
    print('All jobs are completed!')

# %%
"""
### Post-processing
"""

# %%
# retrieve the output
my_list=[]
for node in root.leaves:
    output = tree_maker.from_yaml(node.path+'/output.yaml')
    my_list.append(output['result'])

# %%
# sanity check
assert any(np.array(sorted(my_list))-np.array(my_list_original))==0

# %%
# std of the results
np.std(my_list)

# %%
"""
### Monitoring 
"""

# %%
root=tree_maker.tree_from_yaml(f'/home/jovyan/local_host_home/CERNBox/2021/tree_maker/examples/001_example/study_000/tree.yaml')

# %%
# checking the status
my_filter = lambda node: node.depth==2 and node.has_been('completed')
for node in root.descendants:
    if my_filter(node):
        print(node.path)
        
# one can also use root.find(filter_= lambda node: node.depth==1 and node.has_been('completed'))

# %%
def my_test(node):
    output = tree_maker.from_yaml(node.path+'/output.yaml')
    return node.is_leaf and node.has_been('completed') and output['result']<1.2

for node in root.descendants:
    if my_test(node):
        print(node.path) 

# %%
#or (better)
for node in root.generation(3):
    if my_test(node):
        print(node.path)

# %%
