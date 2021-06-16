from anytree import AnyNode
from anytree.exporter import DictExporter
from anytree.importer import DictImporter
from tree_maker import NodeJob
import yaml # pip install pyyaml 
import ruamel.yaml

ryaml = ruamel.yaml.YAML()

def tree_from_yaml(filename='tree.yaml'): 
    with open(filename, "r") as file:
        return DictImporter(nodecls=NodeJob).import_(yaml.load(file, Loader=yaml.FullLoader))
        
        
def from_yaml(filename):
    try:
        with open(filename, 'r') as file:
            return ryaml.load(file)
    except Exception as e:
        print(e)
        return {}