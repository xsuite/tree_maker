#!/bin/bash
#bsub -q hpc_acc -e %J.err -o %J.out cd $PWD && ./run.sh 
source  /afs/cern.ch/eng/tracking-tools/python_installations/miniconda3/bin/activate  
python run.py
