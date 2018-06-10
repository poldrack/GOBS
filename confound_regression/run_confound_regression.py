# run confound regression on GOBS data

import numpy,pandas
import os,sys
from sklearn.linear_model import LinearRegression

subcode=sys.argv[1].replace('sub-','')

basedir='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
funcdir=os.path.join(basedir,'sub-%s/func'%subcode)
roifile=os.path.join(funcdir,'combined.roidata.txt')
roidata=pandas.read_csv(roifile,sep='\t')
confoundfile=os.path.join(funcdir,'sub-%s_task-rest_run-1_bold_confounds.tsv'%subcode)

# fill NA with zeros - these will be first timepoint
confounds=pandas.read_csv(confoundfile,sep='\t').fillna(0)

# use fd, dvars, acompcor, tcompcor, 
confounds=confounds[['CSF', 'WhiteMatter', 'GlobalSignal', 'stdDVARS', 'FramewiseDisplacement', 'tCompCor00', 'tCompCor01','tCompCor02', 'tCompCor03', 'tCompCor04', 'tCompCor05', 'aCompCor00','aCompCor01', 'aCompCor02', 'aCompCor03', 'aCompCor04', 'aCompCor05','X', 'Y', 'Z','RotX', 'RotY', 'RotZ']]

# fmriprep doesn't include squared motion, so include those
motion=confounds[['X','Y','Z','RotX','RotY','RotZ']]
motion_squared=motion**2
motion_squared.columns=['%s**2'%i for i in motion_squared.columns]

#compute confound regression with GSR

lr=LinearRegression()
lr.fit(confounds,roidata)
residuals=roidata - lr.predict(confounds)
outfile=os.path.join(funcdir,'roidata.confound_resid_GSR.txt')
residuals.to_csv(outfile,index=False,sep='\t')

# run without GSR

confounds_nogsr=confounds.drop('GlobalSignal',axis=1)
lr.fit(confounds_nogsr,roidata)
residuals=roidata - lr.predict(confounds_nogsr)
outfile=os.path.join(funcdir,'roidata.confound_resid_noGSR.txt')
residuals.to_csv(outfile,index=False,sep='\t')
