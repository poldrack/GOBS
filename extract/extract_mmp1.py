# extract data from MMP1 atlas


import os,glob
import nibabel
import numpy


basedir_input='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
subcode='sub-EM2204'

# load atlas surface
atlasdir='/work/01329/poldrack/stampede2/code/GOBS/extract/HCP-MMP1'
atlas={'L':'lh.HCP-MMP1.fsaverage5.gii','R':'rh.HCP-MMP1.fsaverage5.gii'}
atlasdata={}
for a in atlas:
   atlasdata[a]=nibabel.load(os.path.join(atlasdir,atlas[a])).darrays[0].data 

funcfiles={}
for hemis in ['L','R']:
    funcfiles[hemis]=glob.glob(os.path.join(basedir_input,subcode,'func/*task-rest_run-1_bold_space-fsaverage5.%s.func.gii'%hemis))[0]

roidata=numpy.zeros((360,150)) # 360 ROIs by 150 timepoints

for hemis in funcfiles:
    print(hemis,funcfiles[hemis])
    funcdata=nibabel.load(funcfiles[hemis])
    for region in range(1,181):
        
 
