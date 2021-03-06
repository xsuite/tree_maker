import anytree    # pip install anytree 
import subprocess         
from shutil import copytree, copy
import ruamel.yaml # pip install ruamel.yaml 
import yaml        # pip install pyyaml 
import json        # pip install json
from anytree import AnyNode
from anytree.exporter import DictExporter, JsonExporter
from anytree.importer import DictImporter, JsonImporter
from pathlib import Path
import pandas as pd
import tree_maker
import os

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
                 log_file='log.json',
                 dictionary=None):
        super(NodeJobBase, self).__init__()
        self.name = name
        self.parent = parent
        self.path = path
        self.template_path = template_path
        self.submit_command = submit_command
        self.log_file = log_file
        self.dictionary= dictionary
        
        if children:  # set children only if given
            self.children = children
    
   
    def get_abs(self, attribute):
        if attribute == 'path':
            return f"{self.root.dictionary['abs_path']}/{getattr(self, attribute)}"  
        else:
            return f"{self.root.dictionary['abs_path']}/{self.path}/{getattr(self, attribute)}"  
 
 
    def print_it(self):
        '''
        An easy way to print the tree.
        '''
        for pre, _, node in RenderTree(self, style=anytree.render.ContRoundStyle()):
            print(f"{pre}{node.name}")
    
    def submit(self):
        subprocess.call(f'cd {self.get_abs("path")};{self.submit_command}', shell=True)
    
    
    def clone(self):
        if not self.template_path==None:
            copytree(self.get_abs(template_path)+'/config.yaml', child.get_abs('path'))
        else:
            subprocess.call(f'mkdir {self.get_abs(template_path)}', shell=True)
        #self.to_json()
    
    def clone_children(self):
        for child in self.children:
            os.makedirs(child.get_abs('path'), exist_ok=True)
            copy(child.get_abs('template_path')+'/config.yaml', child.get_abs('path')+'/config.yaml')
            #child.to_json()
    
    def rm_children_folders(self,):
        for child in self.children:
            # https://stackoverflow.com/questions/31977833/rm-all-files-under-a-directory-using-python-subprocess-call
            subprocess.call(f'rm -rf {child.get_abs("path")}', shell=True)
                        
    def mutate(self):
        #https://stackoverflow.com/questions/7255885/save-dump-a-yaml-file-with-comments-in-pyyaml
        ryaml = ruamel.yaml.YAML()
        
        self.dictionary['parent'] = self.parent.path
        self.dictionary['log_file'] = self.log_file
        
        with open(self.get_abs('path')+'/config.yaml', 'r') as file:
            cfg = ryaml.load(file)
        for ii in self.dictionary.keys():
            if not type(self.dictionary[ii])==dict:
                # most of case
                cfg[ii]=self.dictionary[ii]
            else:
                # proper partial merging between dict
                # TODO: this works only for 1-depth dict
                cfg[ii]={**cfg[ii], **self.dictionary[ii]}
    
        with open(self.get_abs('path')+'/config.yaml', 'w') as file:
            ryaml.dump(cfg, file)
                
    def clean_log(self):
        if not self.log_file==None:
            my_file = Path(self.log_file)
            if my_file.is_file():
                subprocess.call(f'rm  {self.log_file}', shell=True)
                        
    
    def mutate_children(self):
        for child in self.children:
            child.mutate()
            child.tag_as('mutated')
    
    def to_yaml(self, filename='tree.yaml'): 
        path = self.get_abs('path')
        if not Path(path).is_dir():
            subprocess.call(f'mkdir {path}', shell=True)
        with open(f"{path}/{filename}", "w") as file:  
            yaml.dump(DictExporter().export(self), file)
   
    def to_json(self, filename='tree.json'): 
        path = self.get_abs('path')
        if not Path(path).is_dir():
            subprocess.call(f'mkdir {path}', shell=True)
        with open(f"{path}/{filename}", "w") as file:  
            file.write(JsonExporter(indent=2, sort_keys=True).export(self))
    
    def generation(self, number):
        return [ii for ii in anytree.search.findall(self, 
                filter_=lambda node: node.depth==number)]
    
    def _is_logging_file(self):
        my_file = Path(self.log_file)
        if my_file.is_file():
            return True
        else:
            return False
    
    def has_been(self, tag):
        #if self._is_logging_file():
        if tag in tree_maker.from_json(self.get_abs('path')+'/'+self.log_file).keys():
             return True
        else:
             return False
        #else:
        #    return False 
    
    def has_not_been(self, tag):
        return not self.has_been(tag)
        
    def tag_as(self, tag):
        '''
        This is to tag the node's activity.
        '''
        tree_maker.tag_json.tag_it(self.get_abs('path')+'/'+self.log_file, tag)
        
    def find(self, **kwargs):
        return anytree.search.findall(self,**kwargs)
    
    def cleanlog_mutate_submit(self):
        self.clean_log()

        self.mutate() 
        self.tag_as('mutated')

        self.submit()
        self.tag_as('submitted')
    
    def smart_run(self):
        # if the job has not submitted and
        # its parent is  root or it has been completed
        if self.has_not_been('submitted') and \
            (self.parent.is_root or self.parent.has_been('completed')):
            self.clean_log()

            self.mutate() 
            self.tag_as('mutated')

            self.submit()
            self.tag_as('submitted')
