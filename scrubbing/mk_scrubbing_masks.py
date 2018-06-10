# create scrubbing masks for GOBS data

import numpy,pandas
import os,sys
FDthresh=0.5
timepoints_before=1
timepoints_after=2


subcode=sys.argv[1].replace('sub-','')

basedir='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
funcdir=os.path.join(basedir,'sub-%s/func'%subcode)
roifile=os.path.join(funcdir,'combined.roidata.txt')
roidata=pandas.read_csv(roifile,sep='\t')
confoundfile=os.path.join(funcdir,'sub-%s_task-rest_run-1_bold_confounds.tsv'%subcode)

# fill NA with zeros - these will be first timepoint
confounds=pandas.read_csv(confoundfile,sep='\t').fillna(0)

mask=numpy.ones(confounds.shape[0])
for i,fd in enumerate(confounds['FramewiseDisplacement']):
    if fd > FDthresh:
        print('tp %d: %f'%(i,fd))
        mask[(i-timepoints_before):(i+1+timepoints_after)]=0
outfile=os.path.join(funcdir,'scrubbing_tmask.txt')
numpy.savetxt(outfile,mask)


