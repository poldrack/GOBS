"""
match yeo network assignments to MMP regions
"""

import os
import nibabel
import numpy,pandas
from collections import Counter


# load atlas surface
mmpdir='extract/HCP-MMP1'
mmpatlas={'L':'lh.HCP-MMP1.fsaverage5.gii',
          'R':'rh.HCP-MMP1.fsaverage5.gii'}

yeodir='extract/yeo2011'

yeodict={}
yeodict[7]={0:'Undefined',1:'Visual',2:'Somatomotor',3:'DorsalAttention',
         4:'VentralAttention',5:'Limbic',
         6:'Frontoparietal',7:'Default'}
# from https://www.nature.com/articles/npp201676/tables/1#s1
yeodict[17]={0:'Undefined',
1:'Visual_1',
2:'Visual_2',
3:'Somatomotor_1',
4:'Somatomotor_2',
5:'Attention_1',
6:'Attention_2',
7:'Salience_1',
8:'Salience_2',
9:'Limbic_1',
10:'Limbic_2',
11:'CentralExecutive_1',
12:'CentralExecutive_2',
13:'CentralExecutive_3',
14:'DMN_1',
15:'DMN_2',
16:'DMN_3',
17:'DMN_4'}


surfdir='extract/fsaverage5'
surflocs={'L':nibabel.load(os.path.join(surfdir,'lh.surf.fsaverage5.gii')).darrays[0].data,
          'R':nibabel.load(os.path.join(surfdir,'rh.surf.fsaverage5.gii')).darrays[0].data}

mmpdata={}
mmplabels={}
yeodata={}
yeolabels={}
all_mmp_yeolabels={}
yeodesc={}

for n in [7,17]:
    yeoatlas={'L':'lh.Yeo2011_%dNetworks_N1000.fsaverage5.gii'%n,
              'R':'rh.Yeo2011_%dNetworks_N1000.fsaverage5.gii'%n}

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
    all_mmp_yeolabels[n]=numpy.hstack((mmp_yeolabels['L'][1:],
                                    mmp_yeolabels['R'][1:]))

    yeodesc[n]=[yeodict[n][int(i)] for i in all_mmp_yeolabels[n]]


# now get x/y/z coords for each region
xyzcoords=numpy.zeros((360,3))

for i,a in enumerate(['L','R']):
    for mmpval in numpy.unique(mmpdata[a]):
        if mmpval==0:
            continue
        # get average loc
        mmp_match=mmpdata[a]==mmpval
        mmp_surflocs=surflocs[a][mmp_match,:]
        xyzcoords[(mmpval-1)+i*180,:]=mmp_surflocs.mean(0)


label_df=pandas.DataFrame({'MMP':all_mmplabels,
                           'Yeo7':all_mmp_yeolabels[7],
                           'YeoDesc7':yeodesc[7],
                           'Yeo17':all_mmp_yeolabels[17],
                           'YeoDesc17':yeodesc[17],
                           'X':xyzcoords[:,0],
                           'Y':xyzcoords[:,1],
                           'Z':xyzcoords[:,2]})
# reorder
cols=['MMP','X', 'Y','Z','Yeo7', 'YeoDesc7','Yeo17', 'YeoDesc17']
label_df=label_df[cols]

label_df.to_csv(os.path.join(mmpdir,'MMP_yeo2011_networks.csv'))
