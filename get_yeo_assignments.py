"""
match yeo 7 network assignments to MMP regions
"""

import os
import nibabel
import numpy,pandas
from collections import Counter

# load atlas surface
mmpdir='../extract/HCP-MMP1'
mmpatlas={'L':'lh.HCP-MMP1.fsaverage5.gii',
          'R':'rh.HCP-MMP1.fsaverage5.gii'}
yeodir='../extract/Yeo2011'
yeoatlas={'L':'lh.Yeo2011_7Networks_N1000.fsaverage5.gii',
          'R':'rh.Yeo2011_7Networks_N1000.fsaverage5.gii'}
surfdir='../extract/fsaverage5'
surflocs={'L':nibabel.load(os.path.join(surfdir,'lh.surf.fsaverage5.gii')).darrays[0].data,
          'R':nibabel.load(os.path.join(surfdir,'rh.surf.fsaverage5.gii')).darrays[0].data}
mmpdata={}
mmplabels={}
yeodata={}
yeolabels={}

for a in ['L','R']:
   atlaslabeltable=nibabel.load(os.path.join(mmpdir,mmpatlas[a])).labeltable.labels
   mmplabels[a]=[i.label for i in atlaslabeltable[1:]]
   mmpdata[a]=nibabel.load(os.path.join(mmpdir,mmpatlas[a])).darrays[0].data 
   atlaslabeltable=nibabel.load(os.path.join(yeodir,yeoatlas[a])).labeltable.labels
   yeolabels[a]=[i.label for i in atlaslabeltable[1:]]
   yeodata[a]=nibabel.load(os.path.join(yeodir,yeoatlas[a])).darrays[0].data 
#allatlaslabels=atlaslabels['L']+atlaslabels['R']


mmp_yeolabels={'L':numpy.zeros(181),
               'R':numpy.zeros(181)}


for a in ['L','R']:
    for mmpval in numpy.unique(mmpdata[a]):
        if mmpval==0:
            continue
        yeovals=yeodata[a][mmpdata[a]==mmpval]
        yeovals=yeovals[yeovals>0]
        if len(yeovals)>0:
            counter=Counter(yeovals)
            match=counter.most_common(1)[0][0]
            mmp_yeolabels[a][mmpval]=match
        
all_mmplabels=mmplabels['L']+mmplabels['R']
# need to drop the first element which is the unlabeled regions that are
# excluded from our analyses
all_mmp_yeolabels=numpy.hstack((mmp_yeolabels['L'][1:],
                                mmp_yeolabels['R'][1:]))
yeodict={0:'Undefined',1:'Visual',2:'Somatomotor',3:'DorsalAttention',
         4:'VentralAttention',5:'Limbic',
         6:'Frontoparietal',7:'Default'}
yeodesc=[yeodict[int(i)] for i in all_mmp_yeolabels]


# now get x/y/z coords for each region
xyzcoords={'L':numpy.zeros((3,181)),
               'R':numpy.zeros((3,181))}

for a in ['L','R']:
    for mmpval in numpy.unique(mmpdata[a]):
        if mmpval==0:
            continue
        # get average loc
        

label_df=pandas.DataFrame({'MMP':all_mmplabels,
                           'Yeo':all_mmp_yeolabels,
                           'YeoDesc':yeodesc})
label_df.to_csv(os.path.join(mmpdir,'MMP_yeo2011_7networks.csv'))