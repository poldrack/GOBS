# extract data from MMP1 atlas


import os,glob,sys
import nibabel
import pandas,numpy


basedir_input='/scratch/01329/poldrack/GOBS/GOBS_bids/derivatives/fmriprep'
try:
    subcode=sys.argv[1]
except:
    subcode='sub-EM2204'

# load atlas surface
atlasdir='/work/01329/poldrack/stampede2/code/GOBS/extract/HCP-MMP1'
atlas={'L':'lh.HCP-MMP1.fsaverage5.gii','R':'rh.HCP-MMP1.fsaverage5.gii'}
atlasdata={}
atlaslabels={}
for a in atlas:
   atlaslabeltable=nibabel.load(os.path.join(atlasdir,atlas[a])).labeltable.labels
   atlaslabels[a]=[i.label for i in atlaslabeltable[1:]]
   atlasdata[a]=nibabel.load(os.path.join(atlasdir,atlas[a])).darrays[0].data 
allatlaslabels=atlaslabels['L']+atlaslabels['R']
funcfiles={}
for hemis in ['L','R']:
    funcfiles[hemis]=glob.glob(os.path.join(basedir_input,subcode,'func/*task-rest_run-1_bold_space-fsaverage5.%s.func.gii'%hemis))[0]

roidata=numpy.zeros((360,150)) # 360 ROIs by 150 timepoints
offset={'L':0,'R':180}
for hemis in funcfiles:
    print(hemis,funcfiles[hemis])
    funcdata=nibabel.load(funcfiles[hemis])
    for region in range(180):
       regionverts=atlasdata[hemis]==region+1
       for tp in range(150):
          roidata[region+offset[hemis],tp]=numpy.mean(funcdata.darrays[tp].data[regionverts])

roidata_df=pandas.DataFrame(roidata.T,columns=allatlaslabels)
outfile=os.path.join(basedir_input,subcode,'func/HCP-MMP1.roidata.txt')           
roidata_df.to_csv(outfile,index=False)
#numpy.savetxt(outfile,roidata) 
