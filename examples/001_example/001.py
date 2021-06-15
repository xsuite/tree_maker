# %%
"""
Let aussume that we need to make this computation

$\sqrt{|(a+b)\times c|}$

and we want to compute the standard deviation of the result assuming that a, b and c are normal distributed independent variables. Clearly the problem is quite naive but we want to address is as if we will need a cluster to solve it. 

We can partition the problem in a three conscutive operations
1. A sum: $(a+b)$
2. A multiplication of the result 1 with c: $(a+b)\times c$
3. A sqrt of the result of 2: $\sqrt{|(a+b)\times c|}$
"""

# %%
import tree_maker
from tree_maker import NodeJob

# %%
import numpy as np
a=np.random.randn(4)
b=np.random.randn(4)
c=np.random.randn(2)

my_list_original=[]
for ii in c:
    my_list_original+=list(np.sqrt(np.abs((a+b)*ii)))
my_list_original=sorted(my_list_original)

# %%
#root
root = NodeJob(name='root', parent=None)
# to be modified accordingly
root.path = '/home/jovyan/local_host_home/CERNBox/2021/tree_maker/examples/001_example/study_000'

#first generation
for node in root.leaves:
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node,
                           path = f"{node.path}/{child:03}",
                           template_path = root.path+'/../templates/sum_it',
                           run_command = f'python run.py',
                           dictionary={'a':float(a[child]), 
                                       'b':float(b[child]),
                                       'log_file': f"{node.path}/{child:03}/log.yaml"
                                      })
                   for child in range(len(a))]

#second generation
for node in root.leaves:
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node,
                           path = f"{node.path}/{child:03}",
                           template_path = root.path+'/../templates/multiply_it',
                           run_command = f'python run.py',
                           dictionary={'c':float(c[child]),
                                       'log_file': f"{node.path}/{child:03}/log.yaml",
                                      })
                   for child in range(len(c))]
    
#third generation
for node in root.leaves:
    node.children=[NodeJob(name=f"{child:03}",
                           parent=node, 
                           path = f"{node.path}/{child:03}",
                           template_path = root.path+'/../templates/square_root_it',
                           run_command = f'python run.py',
                           dictionary={'a':float(c[child]),
                                       'log_file': f"{node.path}/{child:03}/log.yaml",
                                       'test': {'guido':4}
                                      })
                           for child in range(1)]
    
root.to_yaml()

# %%
if False:
    for i, node in enumerate(root.leaves):
        if i>3:
            print(i)
            node.run_command = f'condor_submit run.sub -batch-name square_root'

# %%
root.print_it()

# %%
# save the tree
root.to_yaml()

# %%
root.path

# %%
# Load the tree from a yaml
root=tree_maker.tree_from_yaml(f'{root.path}/tree.yaml')
root.print_it()

# %%
root.children[3].children[1].children[0].run_command

# %%
# STEP 1 cloning
root.rm_children()
[x.clone_children() for x in root.generation(0)]
[x.clone_children() for x in root.generation(1)]
[x.clone_children() for x in root.generation(2)];

# %%

#def run_HTCondor(self):
#    import subprocess
#    print('Launching on HTCondor')
#    subprocess.run(f'cd {self.path}; condor_submit run.sub;')
#NodeJob.run_HTCondor=run_HTCondor

for node in root.generation(1):
    node.mutate()
    node.run()

# %%
for node in root.generation(2):
    parent_output = tree_maker.from_yaml(node.parent.path+'/output.yaml')
    node.dictionary['sum_a_b']=parent_output['result']
    node.mutate()
    node.run()

# %%
for node in root.generation(3):
    parent_output = tree_maker.from_yaml(node.parent.path+'/output.yaml')
    node.dictionary['a']=parent_output['result']
    node.mutate()
    node.run()

# %%
my_list=[]
for node in root.generation(3):
    output = tree_maker.from_yaml(node.path+'/output.yaml')
    my_list.append(output['result'])

# %%
assert any(np.array(sorted(my_list))-np.array(my_list_original))==0

# %%
