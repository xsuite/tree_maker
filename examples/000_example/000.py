# %%
"""
### Introduction

We are going to present the `anytree` package that we use for the `tree_maker`.
Please find in the 001_example a proper `tree_maker` example.
"""

# %%
import anytree

# %%
from anytree import AnyNode, RenderTree
root = AnyNode(name="root")
#first generation
[AnyNode(name=f"{ii}", parent=root) for ii in range(2)]
for aa, bb in enumerate(root.children):
    #second generation
    [AnyNode(name=f"{bb.name}{ii}", parent=bb) for ii in range(3)]
    for aa, bb in enumerate(bb.children):
        #third generation
        [AnyNode(name=f"{bb.name}{ii}", parent=bb) for ii in range(2)]
        #...

#print(RenderTree(root))
for pre, _, node in RenderTree(root, style=anytree.render.ContRoundStyle()):
    print(f"{pre}{node.name}")

# %%
# we are commenting it to allow you to use it on /afs
#from anytree.exporter import DotExporter
#DotExporter(root).to_picture('tree.png')

# %%
# Concept of children of a node
[ii.name for ii in  root.children]

# %%
# Concept of parent of a node
# There is a single parent. Is it a limitation? 
# Tree is a "limited" Directed Acycling Graph Directed acyclic graph 
# (https://en.wikipedia.org/wiki/Directed_acyclic_graph)
my_node=root.children[1].children[0]
my_node.name

# %%
my_node.parent.name

# %%
# Concept of ancestors
[ii.name for ii in  my_node.ancestors]

# %%
# Concept of descendants
[ii.name for ii in  my_node.descendants]

# %%
# Concept of sibling
[ii.name for ii in  my_node.siblings]

# %%
# Concept of path
[ii.name for ii in  my_node.path]

# %%
# We can link attribute to a node
my_node.root.name

# %%
# Concept of height of a node
root.height

# %%
# Concept of depth of a node
# This is important to define a "generation"
my_node.depth

# %%
# Concept of leaves of a node
[ii.name for ii in  root.leaves]

# %%
# Search in node and
# select all nodes of a given node depth
# VERY IMPORTANT
[ii.name for ii in anytree.search.findall(root, filter_=lambda node: node.depth==2)]

# %%
# Walk in a tree
w = anytree.walker.Walker()
[ii.name for ii in w.walk(root, root.leaves[0])[-1]]

# %%
# Save the tree in a yaml
import yaml
from anytree import AnyNode
from anytree.exporter import DictExporter
from anytree.importer import DictImporter

dct = DictExporter().export(root)

with open("tree.yaml", "w") as file:  
    yaml.dump(dct, file)

# %%
# Load the tree from a  yaml
with open("tree.yaml", "r") as file:
    root = DictImporter().import_(yaml.load(file, Loader=yaml.FullLoader))
root = DictImporter().import_(dct)
for pre, _, node in RenderTree(root, style=anytree.render.ContRoundStyle()):
    print(f"{pre}{node.name}")

# %%
#%%timeit
# performance 400x30 jobs
from anytree import AnyNode, RenderTree
root = AnyNode(name="root")
#first generation
[AnyNode(name=f"_{ii:03d}", parent=root) for ii in range(400)]
for aa, bb in enumerate(root.children):
    #second generation
    [AnyNode(name=f"__{ii:03d}", parent=bb) for ii in range(30)]

# %%
#%%timeit
[ii.name for ii in anytree.search.findall(root, filter_=lambda node: node.depth==2)]

# %%
"""
We can define a generic class (`JobNode`) that inherits from `anytree` object.
"""

# %%
from anytree import NodeMixin, RenderTree
class JobNodeBase(object):  # Just an example of a base class
    name = 'my_name'
    path = 'my_path'
    #def __repr__(self):
    #        return self.name    
    def __str__(self):
            return self.name
    def run(self):
        pass
    def clone(self):
        pass
    def mutate(self):
        pass

class JobNode(JobNodeBase, NodeMixin):  # Add Node feature
    def __init__(self, name, length, width, parent=None, children=None):
        super(JobNodeBase, self).__init__()
        self.name = name
        self.length = length
        self.width = width
        self.parent = parent
        if children:  # set children only if given
            self.children = children


# %%
root = JobNode('root', length=1, width=2, parent=None)
#first generation
[JobNode(name=f"{ii}", parent=root, length=1, width=2) for ii in range(2)]
for aa, bb in enumerate(root.children):
    #second generation
    [JobNode(name=f"{bb.name}{ii}", parent=bb, length=1, width=2) for ii in range(3)]

for pre, _, node in RenderTree(root, style=anytree.render.ContRoundStyle()):
    print(f"{pre}{node.name}")


# %%
