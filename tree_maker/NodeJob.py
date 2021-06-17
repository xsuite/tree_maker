import anytree    # pip install anytree 
import subprocess         
from shutil import copytree
import ruamel.yaml # pip install ruamel.yaml 
import yaml        # pip install pyyaml 
from anytree import AnyNode
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
from pathlib import Path
import pandas as pd
import tree_maker

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
                 submit_command=None,
                 dictionary = None):
        super(NodeJobBase, self).__init__()
        self.name = name
        self.parent = parent
        self.path = path
        self.template_path = template_path
        self.submit_command = submit_command
        self.dictionary= dictionary
        
        if children:  # set children only if given
            self.children = children
    
    def sum_is_five(x, y):
        '''
        this is an example function to test wether the pytest is working
        '''
        try:
            z = 5
            assert x + y == z
            return True
        except:
            return False

    def print_it(self):
        '''
        An easy way to print the tree.
        '''
        for pre, _, node in RenderTree(self, style=anytree.render.ContRoundStyle()):
            print(f"{pre}{node.name}")
    
    def submit(self):
        subprocess.call(f'cd {self.path};{self.submit_command}', shell=True)
    
    
    def clone(self):
        if not self.template_path==None:
            copytree(self.template_path, child.path)
        else:
            subprocess.call(f'mkdir {self.path}', shell=True)
        self.to_yaml()
    
    def clone_children(self):
        for child in self.children:
            copytree(child.template_path, child.path)
            child.to_yaml()
    
    def rm_children_folders(self,):
        for child in self.children:
            # https://stackoverflow.com/questions/31977833/rm-all-files-under-a-directory-using-python-subprocess-call
            subprocess.call(f'rm -rf {child.path}', shell=True)
                        
    def mutate(self):
        #https://stackoverflow.com/questions/7255885/save-dump-a-yaml-file-with-comments-in-pyyaml
        ryaml = ruamel.yaml.YAML()
        
        with open(self.path+'/config.yaml', 'r') as file:
            cfg = ryaml.load(file)
        for ii in self.dictionary.keys():
            if not type(self.dictionary[ii])==dict:
                # most of case
                cfg[ii]=self.dictionary[ii]
            else:
                # proper partial merging between dict
                # TODO: this works only for 1-depth dict
                cfg[ii]={**cfg[ii], **self.dictionary[ii]}
    
        with open(self.path+'/config.yaml', 'w') as file:
            ryaml.dump(cfg, file)
                
    def clean_log(self):
        my_file = Path(self.dictionary['log_file'])
        if my_file.is_file():
            subprocess.call(f'rm  {self.dictionary["log_file"]}', shell=True)
                        
    
    def mutate_children(self):
        for child in self.children:
            child.mutate()
    
    def to_yaml(self, filename='tree.yaml'): 
        if not Path(self.path).is_dir():
            subprocess.call(f'mkdir {self.path}', shell=True)
        with open(f"{self.path}/{filename}", "w") as file:  
            yaml.dump(DictExporter().export(self), file)
   
    def generation(self, number):
        return [ii for ii in anytree.search.findall(self, 
                filter_=lambda node: node.depth==number)]
    
    def _is_logging_file(self):
        my_file = Path(self.dictionary['log_file'])
        if my_file.is_file():
            return True
        else:
            return False
    
    def has_been(self, tag):
        if self._is_logging_file:
            my_df= pd.DataFrame(tree_maker.from_yaml(self.dictionary['log_file'])).transpose()
            if tag in my_df['tag'].values:
                return True
            else:
                return False
        else:
            return False 
    
    def has_not_been(self, tag):
        return not self.has_been(tag)
        
    def tag_as(self, tag):
        tree_maker.tag.tag_it(self.dictionary['log_file'], tag)
        
    def find(self, **kwargs):
        return anytree.search.findall(self,**kwargs)
    
    def cleanlog_mutate_submit(self):
        self.clean_log()

        self.tag_as('mutated')
        self.mutate() 

        self.tag_as('submitted')
        self.submit()
        




