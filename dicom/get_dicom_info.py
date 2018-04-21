"""
load dicom dirs and record what's in them
"""

import os,glob
import pydicom
import pickle


basedir='/Users/poldrack/data_unsynced/GOBS/GOBS_dicom'
basedir='/scratch/01329/poldrack/GOBS/GOBS_dicom'
dcmdirs=glob.glob(os.path.join(basedir,'*'))

dcminfo={}
for d in dcmdirs:
    subcode=os.path.basename(d)
    dcminfo[d]={}
    scans=glob.glob(os.path.join(d,'SCANS/*'))
    for s in scans:
        scannum=os.path.basename(s)
        dcmfiles=glob.glob(os.path.join(s,'DICOM/*_*.dcm'))
        if len(dcmfiles)==0:
            dcminfo[d][scannum]=(None,0)
        else:
            ds = pydicom.dcmread(dcmfiles[1])
            dcminfo[d][scannum]=ds.ProtocolName

with open('dcminfo.pkl','wb') as f:
    pickle.dump(dcminfo,f)
