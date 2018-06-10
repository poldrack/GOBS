"""
make singularity command to convert aseg to mni
"""

import os,sys
import glob

basedir='/scratch/01329/poldrack/GOBS'
derivbase=os.path.join(basedir,'GOBS_bids/derivatives/fmriprep')
workbase=os.path.join(basedir,'workdir/fmriprep/fmriprep_wf')


subcodes=[os.path.basename(i).replace('sub-','') for i in glob.glob(os.path.join(derivbase,'sub*')) if not i.find('html')>-1]
for subcode in subcodes:
    derivdir=os.path.join(derivbase,'sub-%s'%subcode)
    workdir=os.path.join(workbase,'single_subject_%s_wf/anat_preproc_wf/t1_2_mni'%subcode)
    infile=os.path.join(derivdir,'anat/sub-%s_T1w_label-aseg_roi.nii.gz'%subcode)
    outfile=os.path.join(derivdir,'anat/sub-%s_T1w_label-aseg_roi_MNI152Lin2009cAsym.nii.gz'%subcode)
    reffile=os.path.join(workdir,'ants_t1_to_mni_Warped.nii.gz')
    transformfile=os.path.join(workdir,'ants_t1_to_mniComposite.h5')
    cmd='PYTHONPATH="" singularity exec /work/03843/crn_plab/singularity/poldracklab_fmriprep_1.0.11-2018-04-16-76a455b6e61f.img antsApplyTransforms -v 1 -d 3 -i %s -o %s -r %s -n NearestNeighbor -t %s'%(infile,outfile,reffile,transformfile)
    print(cmd)
