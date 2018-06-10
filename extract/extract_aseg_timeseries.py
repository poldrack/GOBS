"""
use aseg labels to extract and save timeseries
"""


import os,sys
from nilearn.input_data import NiftiLabelsMasker
import pandas,numpy
import nibabel

label_fields={10:'Left-Thalamus-Proper',
11:'Left-Caudate',
12:'Left-Putamen',
13:'Left-Pallidum',
17:'Left-Hippocampus',
18:'Left-Amygdala',
26:'Left-Accumbens-area',
49:'Right-Thalamus-Proper',
50:'Right-Caudate',
51:'Right-Putamen',
52:'Right-Pallidum',
53:'Right-Hippocampus',
54:'Right-Amygdala',
58:'Right-Accumbens-area'}

subcode=sys.argv[1].replace('sub-','')

basedir='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
anatdir=os.path.join(basedir,'sub-%s/anat'%subcode)
funcdir=os.path.join(basedir,'sub-%s/func'%subcode)
labelfile=os.path.join(anatdir,'sub-%s_T1w_label-aseg_roi_MNI152Lin2009cAsym.nii.gz'%subcode)
funcfile=os.path.join(funcdir,'sub-%s_task-rest_run-1_bold_space-MNI152NLin2009cAsym_preproc.nii.gz'%subcode)
masker=NiftiLabelsMasker(labels_img=labelfile,standardize=False)
tsdata=masker.fit_transform(funcfile)
labelimg=nibabel.load(labelfile)
labels=numpy.unique(labelimg.get_data()).astype('int')
keepidx=[]
for i,l in enumerate(labels):
    if l in label_fields.keys():
        keepidx.append(i)

tsdata_df=pandas.DataFrame(tsdata)
tsdata_keep_df=tsdata_df.iloc[:,keepidx]
tsdata_keep_df.columns=[label_fields[labels[i]] for i in keepidx]
outfile=os.path.join(funcdir,'aseg.roidata.txt')
tsdata_keep_df.to_csv(outfile,index=False)

