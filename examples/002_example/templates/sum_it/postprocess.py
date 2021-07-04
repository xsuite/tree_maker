import glob
import awkward as ak
import numpy as np

my_folders=sorted(glob.glob('0*')) 
my_list=[]
for my_folder in my_folders:
    aux=ak.from_parquet(f'{my_folder}/test.parquet')
    my_list.append(np.mean(aux))
aux=ak.Array(my_list)
ak.to_parquet(aux,'./summary.parquet')
