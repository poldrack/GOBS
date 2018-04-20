import os,glob
basedir='/scratch/01329/poldrack/GOBS/GOBS_bids'

# first find empty dirs or dirs without anat or func
bidsdirs=[i for i in glob.glob(os.path.join(basedir,'*')) if os.path.isdir(i)]
empty=[]
nodata=[]
gooddata=[]
for b in bidsdirs:
    files=glob.glob(os.path.join(b,'*'))

    if len(files)==0:
        empty.append(b)
        continue
    dnames=[os.path.basename(i) for i in files]
    if not 'anat' in dnames and not 'func' in dnames:
        nodata.append(b)
    else:
        gooddata.append(os.path.basename(b))

if len(empty)>0 or len(nodata)>0:
  with open('cleanup_bids_dirs.sh','w') as f:
    f.write('#empty directories\n')
    for i in empty:
        f.write('rm -rf %s\n'%i)
    f.write('#directories without data\n')
    for i in nodata:
        f.write('rm -rf %s\n'%i)

# check list of files against participants list
import pandas
pinfo=pandas.read_csv('/scratch/01329/poldrack/GOBS/participants.tsv.older',
        sep='\t')
pinfo['goodsub']=0
for i in range(pinfo.shape[0]):
   if pinfo.iloc[i,0] in gooddata:
        pinfo.loc[i,'goodsub']=1 
pinfo=pinfo.query('goodsub==1')
pinfo.to_csv('/scratch/01329/poldrack/GOBS/GOBS_bids/participants.tsv',
    sep='\t',index=False)
