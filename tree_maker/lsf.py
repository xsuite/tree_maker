
import pandas as pd
import subprocess
from io import StringIO
import tree_maker as tm

def bjobs():
    out = subprocess.Popen(['bjobs','-o', "jobid stat command user FROM_HOST EXEC_HOST JOB_NAME SUBMIT_TIME queue project application mem delimiter=','"],
          stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate() 
    if stdout==b'No unfinished job found\n':
        return pd.DataFrame()
    else:
        return pd.read_csv(StringIO(stdout.decode('UTF-8')), sep=',')

# from Hamish
def get_status(node):
    """
    Returns last key, the status of the job, from 'log_file'. Incase of an empty log_file, 'None' is returned.
    """
    keys = list(tm.from_json(node.get_abs('path')+'/'+node.log_file))
    if len(keys) > 0:
        return keys[-1]
    else:
        return None
    
def create_df(node):
    """
    Creating a dataframe and its attributes. Here its attributes are; node, path, x_values, y_values and my_colors.
    """
    my_df = pd.DataFrame([node]+list(node.descendants), columns=['handle']).copy()
    my_df['name'] = my_df['handle'].apply(lambda x:x.name)
    my_df['path'] = my_df['handle'].apply(lambda x:x.get_abs('path'))
    my_df['status'] = my_df['handle'].apply(get_status)
    return my_df

