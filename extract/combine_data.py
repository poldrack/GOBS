# combine MMP and aseg

import os,sys
import pandas

#subcode=sys.argv[1].replace('sub-','')
subcode='EJ0093'

basedir='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
funcdir=os.path.join(basedir,'sub-%s/func'%subcode)

mmpdata=pandas.read_csv(os.path.join(funcdir,'HCP-MMP1.roidata.txt'))
asegdata=pandas.read_csv(os.path.join(funcdir,'aseg.roidata.txt'))
combined=pandas.concat([mmpdata,asegdata],axis=1)
outfile=os.path.join(funcdir,'combined.roidata.txt')
combined.to_csv(outfile,index=False,sep='\t')

