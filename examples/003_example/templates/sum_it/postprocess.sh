#!/bin/bash
#bsub -q hpc_acc -e %J.err -o %J.out cd $PWD && ./run.sh 
source  /afs/cern.ch/eng/tracking-tools/python_installations/miniconda3/bin/activate  
python /gpfs/gpfs/gpfs_maestro_home_new/hpc/sterbini/tree_maker/examples/002_example/templates/sum_it/postprocess.py
