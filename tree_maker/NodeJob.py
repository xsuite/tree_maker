import anytree    # pip install anytree 
import subprocess         
from shutil import copytree
import ruamel.yaml # pip install ruamel.yaml 
import yaml        # pip install pyyaml 
from anytree import AnyNode
from anytree.exporter import DictExporter
from anytree.importer import DictImporter

from anytree import AnyNode, NodeMixin, RenderTree
class NodeJobBase(object):  # Just an example of a base class
    name = None
    path = None
    def __str__(self):
            return self.name

class NodeJob(NodeJobBase, NodeMixin):  # Add Node feature
    def __init__(self, parent=None, children=None, name= None,
                 path=None,
                 template_path=None, 
                 run_command=None,
                 dictionary = None):
        super(NodeJobBase, self).__init__()
        self.name = name
        self.parent = parent
        self.path = path
        self.template_path = template_path
        self.run_command = run_command
        self.dictionary= dictionary
        
        if children:  # set children only if given
            self.children = children
    
    def print_it(self):
        '''
        An easy way to print the tree.
        '''
        for pre, _, node in RenderTree(self, style=anytree.render.ContRoundStyle()):
            print(f"{pre}{node.name}")
    
    def run(self):
        subprocess.call(f'cd {self.path};{self.run_command}', shell=True)
        
    def clone_children(self):
        for child in self.children:
            copytree(child.template_path, child.path)
            child.to_yaml()
    
    def rm_children(self,):
        for child in self.children:
            # https://stackoverflow.com/questions/31977833/rm-all-files-under-a-directory-using-python-subprocess-call
            subprocess.call(f'rm -rf {child.path}', shell=True)
                        
    def mutate(self):
        #https://stackoverflow.com/questions/7255885/save-dump-a-yaml-file-with-comments-in-pyyaml
        ryaml = ruamel.yaml.YAML()
        
        with open(self.path+'/config.yaml', 'r') as file:
            cfg = ryaml.load(file)
        for ii in self.dictionary.keys():
            cfg[ii]=self.dictionary[ii]
    
        with open(self.path+'/config.yaml', 'w') as file:
            ryaml.dump(cfg, file)
                        
    def mutate_children(self):
        for child in self.children:
            child.mutate()
    
    def to_yaml(self, filename='tree.yaml'): 
        with open(f"{self.path}/{filename}", "w") as file:  
            yaml.dump(DictExporter().export(self), file)
   
    def generation(self, number):
        return [ii for ii in anytree.search.findall(self, 
                filter_=lambda node: node.depth==number)]

def from_yaml(filename='tree.yaml'): 
        with open("tree.yaml", "r") as file:
            return DictImporter(nodecls=NodeJob).import_(yaml.load(file, Loader=yaml.FullLoader))