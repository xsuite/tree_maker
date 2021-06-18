import collections
import ruamel.yaml
import datetime
import json
from collections import OrderedDict

#the three functions we need:
def tag_first(myfile, mycomment):
    """
    tag_first is to overwrite an already existing yaml file or
    create a new yaml file and add the first timestamps.

    Examples
    --------
    >>> tag_first('myfile', 'hello')

    If 'my_file' already exits, it will overwrite that file and create a first timestamp.
    """
        
    stage = 0
    with open(myfile, 'w') as file:
        yaml = ruamel.yaml.YAML() 
        my_dict = {stage: {}}
        my_dict[stage]['tag'] = mycomment
        my_dict[stage]['unix_time'] = datetime.datetime.now().timestamp()        #in seconds
        my_dict[stage]['human_time'] = datetime.datetime.now()
        yaml.dump(my_dict, file)

def read_yaml(myfile, verbose=False):
    """
    read_yaml is to read a yaml file and convert it into python.

    Example
    --------
    >>> read_yaml('mytest.yml')

    This will return the contents inside of a yaml file.
    """
    try: 
        with open(myfile, 'r') as file:
            yaml = ruamel.yaml.YAML()    
            my_dict = yaml.load(file)
        return my_dict
    except FileNotFoundError:
        if verbose: print('New file created.')
        my_dict = {}
        return my_dict
    except ruamel.yaml.constructor.DuplicateKeyError:
        my_dict = {}
        return my_dict
    except Exception as e: 
        print(e.__class__)
        return None

def convert_to_dict(input_dict):
    my_dict = OrderedDict(input_dict)
    output_dict = json.loads(json.dumps(my_dict))
    return output_dict

#creating a yaml file using tag_first, then reading it
tag_first('example_file.yaml', 'hello')

a = read_yaml('example_file.yaml')

print(a)

#converting the ordereddict to a dict

convert_to_dict(a)