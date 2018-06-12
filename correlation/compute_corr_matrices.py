"""
compute correlation matrix for each subject
with and without GSR and scrubbing

"""


import os,glob
import numpy,pandas
import pickle

basedir='/Users/poldrack/data_unsynced/GOBS/roidata'

subdirs=glob.glob(os.path.join(basedir,'sub-*'))

data={}
corrs={}

def getcorr(d,tmask=None,verbose=False):
    """
    return upper triangle of correlation matrix
    with scrubbing if tmask is specified
    """
    if type(d) == pandas.core.frame.DataFrame:
        d=d.values
    if tmask is None:
        tmask=numpy.ones(d.shape[0])
    assert tmask.shape[0]==d.shape[0]
    cc=numpy.corrcoef(d[tmask==1,:].T)
    if verbose:
        print('size:',d[tmask==1,:].shape)
        print('number of scrubbed points:',numpy.sum(tmask==0))
    return (cc[numpy.triu_indices_from(cc,1)])
    
for subdir in subdirs:
    subcode=os.path.basename(subdir)
    data[subcode]={}
    data[subcode]['GSR']=pandas.read_csv(os.path.join(subdir,
                        'func/roidata.confound_resid_GSR.txt'),sep='\t')
    data[subcode]['noGSR']=pandas.read_csv(os.path.join(subdir,
                        'func/roidata.confound_resid_noGSR.txt'),sep='\t')
    data[subcode]['tmask']=numpy.loadtxt(os.path.join(subdir,
                        'func/scrubbing_tmask.txt'))
    data[subcode]['nscrubbed']=numpy.sum(data[subcode]['tmask']==0)
    
    corrs[subcode]={}
    corrs[subcode]['noGSR']=getcorr(data[subcode]['noGSR'])
    corrs[subcode]['GSR']=getcorr(data[subcode]['GSR'])
    corrs[subcode]['GSR+scrub']=getcorr(data[subcode]['GSR'],
         tmask=data[subcode]['tmask'])
    corrs[subcode]['nscrubbed']=data[subcode]['nscrubbed']
   
pickle.dump(data,open(os.path.join(basedir,'data.pkl'),'wb'))
pickle.dump(corrs,open(os.path.join(basedir,'corrs.pkl'),'wb'))
