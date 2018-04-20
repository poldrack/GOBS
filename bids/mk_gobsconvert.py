# make conversion script for all subjects

import os,glob


basedir='/scratch/01329/poldrack/GOBS/GOBS_nii'
subcodes=[os.path.basename(i) for i in glob.glob(os.path.join(basedir,'*'))]

with open('convert_to_bids.sh','w') as f:
    for s in subcodes:
        f.write('python convert_bids.py %s\n'%s)

