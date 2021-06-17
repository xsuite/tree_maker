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
# Load the tree from a yaml
try:
    root=tree_maker.tree_from_yaml(
    f'/home/jovyan/local_host_home/CERNBox/2021/tree_maker/examples/001_example/study_000/tree.yaml')
except Exception as e:
    print(e)
    print('Probably you forgot to edit the address of you yaml file...')


def smart_run(self):
    if self.has_not_been('submitted') and \
        (self.parent.is_root or self.parent.has_been('completed')):
        self.clean_log()

        self.tag_as('mutated')
        self.mutate() 

        self.tag_as('submitted')
        self.submit()

NodeJob.smart_run = smart_run

if root.has_been('completed'):
    print('All descendants of root are completed!')
else:
    for node in root.descendants:
        node.smart_run()
    if all([descendant.has_been('completed') for descendant in root.descendants]):
        root.tag_as('completed')