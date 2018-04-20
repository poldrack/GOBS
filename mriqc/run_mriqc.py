"""
run mriqc on all datsets in GOBS

singularity run  MRIWC /scratch/01329/poldrack/GOBS/GOBS_bids /scratch/01329/pold
rack/GOBS/GOBS_bids/derivatives participant --participant_label sub-EQ0058 -m bo
ld --nprocs 32 --mem_gb 64 --ants-nthreads 8 --ants-float --ica
/work/03843/crn_plab/singularity/poldracklab_mriqc_0.10.4-2018-03-23-f1e4d594153
3.img /scratch/01329/poldrack/GOBS/GOBS_bids /scratch/01329/poldrack/GOBS/GOBS_b
ids/derivatives participant --participant_label sub-EQ0058 -m T1w --nprocs 16 --
mem_gb 64 --ants-nthreads 8 --ants-float

"""

import os
from bids.grabbids import BIDSLayout

project_root = '/scratch/01329/poldrack/GOBS/GOBS_bids'
layout = BIDSLayout(project_root)

MRIQC='/work/03843/crn_plab/singularity/poldracklab_mriqc_0.10.4-2018-03-23-f1e4d5941533.img'
derivdir=os.path.join(project_root,'derivatives')

t1data=layout.get(type='T1w',target='subject',return_type='id')

with open('mriqc_T1w.sh','w') as f:
    for subcode in t1data:
        cmd='singularity run %s %s %s participant --participant_label sub-%s -m T1w --nprocs 16 --mem_gb 64 --ants-nthreads 8 --ants-float'%(MRIQC,
                project_root,derivdir,subcode)
        f.write(cmd+'\n')

bolddata=layout.get(type='bold',target='subject',return_type='id')

with open('mriqc_bold.sh','w') as f:
    for subcode in bolddata:
        cmd='singularity run %s %s %s participant --participant_label sub-%s -m bold --ica --nprocs 32 --mem_gb 64 --ants-nthreads 8 --ants-float'%(MRIQC,
                project_root,derivdir,subcode)
        f.write(cmd+'\n')
